from __future__ import absolute_import
import logging
from collections import defaultdict
import re

from aleph.core import db
from aleph.model import Reference, Entity
from aleph.model.entity_details import EntityIdentifier
from aleph.analyze.analyzer import Analyzer


log = logging.getLogger(__name__)

DEFAULT_SCHEMA = '/entity/company.json#'


class Company(Analyzer):

    origin = 'za_company'

    def prepare(self):
        self.collections = []
        for collection in self.document.collections:
            if collection.generate_entities:
                self.collections.append(collection)
        self.disabled = not len(self.collections)
        self.entities = defaultdict(list)
        log.info("za_company init")

    def on_text(self, text):
        if self.disabled or text is None:
            return
        regexp = '([A-Z][\w]*\.?(\s+[A-Z\(][\w\-@\.#&!\(\)]*)*\s+' + \
                 '\(Reg\w*\.? [Nn]\w+\.? (\d{4}/\d+/\d{2})\))'
        flags = re.MULTILINE
        log.info("za_entities start")
        matches = re.findall(regexp, text, flags)
        for match in matches:
            full = re.sub('\s+', ' ', match[0], flags=re.MULTILINE)
            log.info("%s  %s" % (match[2], full))
        log.info("za_entities stop")

    def load_entity(self, name, schema):
        identifier = name.lower().strip()
        q = db.session.query(EntityIdentifier)
        q = q.order_by(EntityIdentifier.deleted_at.desc().nullsfirst())
        q = q.filter(EntityIdentifier.scheme == self.origin)
        q = q.filter(EntityIdentifier.identifier == identifier)
        ident = q.first()
        if ident is not None:
            if ident.deleted_at is None:
                # TODO: add to collections? Security risk here.
                return ident.entity_id
            if ident.entity.deleted_at is None:
                return None

        data = {
            'name': name,
            '$schema': schema,
            'state': Entity.STATE_PENDING,
            'identifiers': [{
                'scheme': self.origin,
                'identifier': identifier
            }]
        }
        entity = Entity.save(data, self.collections)
        return entity.id

    def finalize(self):
        if self.disabled:
            return

        output = []
        for entity_name, schemas in self.entities.items():
            schema = max(set(schemas), key=schemas.count)
            output.append((entity_name, len(schemas), schema))

        self.document.delete_references(origin=self.origin)
        for name, weight, schema in output:
            entity_id = self.load_entity(name, schema)
            if entity_id is None:
                continue
            ref = Reference()
            ref.document_id = self.document.id
            ref.entity_id = entity_id
            ref.origin = self.origin
            ref.weight = weight
            db.session.add(ref)
        log.info('za_companies extraced %s entities.', len(output))
