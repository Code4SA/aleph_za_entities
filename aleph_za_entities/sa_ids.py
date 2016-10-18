from __future__ import absolute_import
import logging
import re
import luhn

from aleph.core import db
from aleph.model import Reference, Entity
from aleph.model.entity_details import EntityIdentifier
from aleph.analyze.analyzer import Analyzer

log = logging.getLogger(__name__)

DEFAULT_SCHEMA = '/entity/person.json#'
# something like Forename Forename etc Lastname, SA_ID_NR & SA_ID_NR
# Match another SA ID number separated by &, / or and so we can
# skip partnerships to start with and not assign the wrong ID to the wrong
# person
REGEX = """
(                                # Start full capture
(                                # Start full name capture
(                                # Start first word capture
[A-Z][-\w\']*|                   # First word starts with caps
v[ao]n|de[nr]?|du|le             # or is one of the common surname prefixes
)                                # End first word capture
(,?                              # Start subsequent word count control
\s[A-Z][\w\'-]+|                 # Subsequent words start with caps
\sv[ao]n|\sde[nr]?|\sdu|\sle     # or is one of the common surname prefixes
)+                               # End subsequent word count control
),                               # End full name capture, require comma
\s(\d{13})                       # Capture 13 digits for SA ID number
(\s?[/&]?(and)?\s?\d{10,15})?    # Optionally capture a second ID separated by and or &
)                                # End full capture
"""


class Person(object):
    def __init__(self, name, id, presentation):
        self.name = name
        self.id = id
        self.presentation = presentation

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.presentation)


class PersonExtractor(object):
    def __init__(self):
        self.regex = re.compile(REGEX, re.VERBOSE + re.MULTILINE)

    def on_text(self, text):
        cleantext = re.sub('\s+', ' ', text, flags=re.MULTILINE)
        matches = self.regex.findall(cleantext)
        persons = []
        for match in matches:
            if match[5]:
                # Skip partnerships
                continue
            sa_id = match[4]
            if not is_valid_sa_id(sa_id):
                log.debug("Skipping invalid SA ID %s" % sa_id)
                continue
            presentation = match[0]
            name = match[1]
            persons.append(Person(name, sa_id, presentation))
        return persons


class PersonAnalyzer(Analyzer):
    scheme = 'sa_id'
    origin = 'za_persons'

    def __init__(self, *args, **kwargs):
        super(PersonAnalyzer, self).__init__(*args, **kwargs)
        self.entities = []
        self.extractor = PersonExtractor()
        self.text_count = 0

    def prepare(self):
        self.collections = []
        for collection in self.document.collections:
            if collection.generate_entities:
                self.collections.append(collection)
        self.disabled = not len(self.collections)

    def on_text(self, text):
        log.debug("%s text index %d", self, self.text_count)
        self.text_count += 1
        cleantext = re.sub('\s+', ' ', text, flags=re.MULTILINE)
        for person in self.extractor.on_text(cleantext):
            self.entities.append((person.id, person.name, person.presentation))

    def load_entity(self, sa_id, name, full):
        identifier = sa_id
        log.debug("%s Loading %s %s", self, self.scheme, sa_id)
        q = db.session.query(EntityIdentifier)
        q = q.order_by(EntityIdentifier.deleted_at.desc().nullsfirst())
        q = q.filter(EntityIdentifier.scheme == self.scheme)
        q = q.filter(EntityIdentifier.identifier == identifier)
        ident = q.first()
        if ident is not None:
            if ident.deleted_at is None:
                # TODO: add to collections? Security risk here.
                return ident.entity_id
            if ident.entity.deleted_at is None:
                return None

        data = {
            'name': full,
            '$schema': DEFAULT_SCHEMA,
            'identifiers': [{
                'scheme': self.scheme,
                'identifier': identifier
            }],
            'other_names': [
                {'name': name},
                {'name': sa_id},
            ],
            'company_number': sa_id
        }
        log.debug("%s Saving %s", self, full)
        entity = Entity.save(data, self.collections)
        return entity.id

    def finalize(self):
        if self.disabled:
            return
        log.debug("%s deleting old refs for document %d", self, self.document.id)
        self.document.delete_references(origin=self.origin)
        for sa_id, name, full in self.entities:
            log.debug("%s Linking %s to document %d", self, sa_id, self.document.id)
            entity_id = self.load_entity(sa_id, name, full)
            ref = Reference()
            ref.document_id = self.document.id
            ref.entity_id = entity_id
            ref.origin = self.origin
            ref.weight = 1
            db.session.add(ref)
        log.info('za_persons extraced %s entities.', len(self.entities))


def is_valid_sa_id(id):
    return luhn.verify(id) and len(id) == 13
