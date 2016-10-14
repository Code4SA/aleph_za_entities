from __future__ import absolute_import
import logging
import re

from aleph.core import db
from aleph.model import Reference, Entity
from aleph.model.entity_details import EntityIdentifier
from aleph.analyze.analyzer import Analyzer


log = logging.getLogger(__name__)

DEFAULT_SCHEMA = '/entity/company.json#'
REGEX = """
(                              # Start full name and ID capture
(                              # Start name capture
[A-Z][\w]*\.?                  # First name word must start with caps but can be abbreviated with .
(                              # Start multiple subsequent word parens to control number
\s+[A-Z\(][\w\-@\.#&!\(\)/]*|  # Subsequent name words must start with caps or be one of
\s+and|                        # - "and"
\s+en|                         # - "and" in afrikaans - TODO add more languages
\s+\d+|                        # - some integer
\s+t/a                         # - abbvreviated "trading as"
)+                             # Finish subsequent name count control
)\s+                           # Finish name capture
\(                             # Start matching Reg no in parens
Reg\w*\.?\s+[Nn]\w+\.?\s+        # Various ways of writing "Registration number"
(\d{4}/\d+/\d{2})              # Capture post-1951 style company reg numbers
\)                             # Finish Reg no in parens
)                              # Finish full name and ID capture
"""

class Company(Analyzer):
    scheme = 'sacipc'
    origin = 'za_company'

    def __init__(self, *args, **kwargs):
        super(Company, self).__init__(*args, **kwargs)
        self.entities = []
        self.re = re.compile(REGEX, re.VERBOSE)

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
            regno = match[3]
            full = re.sub('\s+', ' ', match[0], flags=re.MULTILINE)
            name = re.sub('\s+', ' ', match[1], flags=re.MULTILINE)
            self.entities.append((regno, name, full))

    def load_entity(self, regno, name, full):
        identifier = regno
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
                {'name': regno},
            ],
            'company_number': regno
        }
        entity = Entity.save(data, self.collections)
        return entity.id

    def finalize(self):
        if self.disabled:
            return

        self.document.delete_references(origin=self.origin)
        for regno, name, full in self.entities:
            entity_id = self.load_entity(regno, name, full)
            ref = Reference()
            ref.document_id = self.document.id
            ref.entity_id = entity_id
            ref.origin = self.origin
            ref.weight = 1
            db.session.add(ref)
        log.info('za_companies extraced %s entities.', len(self.entities))
