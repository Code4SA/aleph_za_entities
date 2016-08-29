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
REGEX = '(([A-Z][-\w\']*(\s+[A-Z][\w\'-]+|\s+v[ao]n|\s+de[nr]?)*),' + \
        '\s+(\d{13})(\s*[/&]?(and)?\s*\d{10,15})?)'


class Persons(Analyzer):
    scheme = 'sacipc'
    origin = 'za_persons'

    def __init__(self, *args, **kwargs):
        super(Persons, self).__init__(*args, **kwargs)
        self.entities = []
        self.re = re.compile(REGEX)

    def prepare(self):
        self.collections = []
        for collection in self.document.collections:
            if collection.generate_entities:
                self.collections.append(collection)
        self.disabled = not len(self.collections)

    def on_text(self, text):
        if self.disabled or text is None:
            return
        flags = re.MULTILINE
        matches = self.re.findall(text, flags)
        for match in matches:
            if match[4]:
                # Skip partnerships
                continue
            sa_id = match[3]
            if not is_valid_sa_id(sa_id):
                log.debug("Skipping invalid SA ID %s" % sa_id)
                continue
            full = re.sub('\s+', ' ', match[0], flags=re.MULTILINE)
            name = re.sub('\s+', ' ', match[1], flags=re.MULTILINE)
            self.entities.append((sa_id, name, full))

    def load_entity(self, sa_id, name, full):
        identifier = "%s:%s" % (self.scheme, sa_id)
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
                'identifier': sa_id
            }],
            'other_names': [
                {'name': name},
                {'name': sa_id},
            ],
            'company_number': sa_id
        }
        entity = Entity.save(data, self.collections)
        return entity.id

    def finalize(self):
        if self.disabled:
            return

        self.document.delete_references(origin=self.origin)
        for sa_id, name, full in self.entities:
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
