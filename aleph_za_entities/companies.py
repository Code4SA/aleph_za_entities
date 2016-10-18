# -*- coding: utf-8 -*-

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
[A-Z][\w\.]*                   # First name word must start with caps but can be abbreviated with .
(                              # Start multiple subsequent word parens to control number
                               # Subsequent name words must be one of
\sand|                         # - "and"
\sen|                          # - "and" in afrikaans - TODO add more languages
\st/a|                         # - abbvreviated "trading as"
\s\([a-zA-Z]+\)|
\s[\wé\-@\.#&!/’]+|            # - letters possibly connected to some punctuation
){1,9}                         # Finish subsequent name count control
)\s                            # Finish name capture
\(                             # Start matching Reg no in parens
Reg\w*\.?\s[Nn]\w+\.?\s        # Various ways of writing "Registration number"
(\d{4}/\d+/\d{2})              # Capture post-1951 style company reg numbers
\)                             # Finish Reg no in parens
)                              # Finish full name and ID capture
"""

# Names to skip because they're incorrect and need "very domain/doc-specific"
# regexing or coding to support properly for some currently subjective
# definition of that.
# Rather than go down the road of coding domain/doc-specific entity extraction
# here, let's leave that for scrapers of those domains/documents.
NAME_BLACKLIST = [
    'Applicant'
]


class Company(object):
    def __init__(self, name, regno, fullname):
        self.name = name
        self.regno = regno
        self.fullname = fullname

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self.fullname)


class CompanyExtractor(object):
    def __init__(self):
        self.regex = re.compile(REGEX, re.VERBOSE + re.MULTILINE)

    def on_text(self, text):
        cleantext = re.sub('\s+', ' ', text, flags=re.MULTILINE)
        matches = self.regex.findall(cleantext)
        companies = []
        for match in matches:
            regno = match[3].strip()
            fullname = match[0].strip()
            name = match[1].strip()
            if name in NAME_BLACKLIST or \
               len(name.split()) <= 1:
                continue
            companies.append(Company(name, regno, fullname))
        return companies


class CompanyAnalyzer(Analyzer):
    scheme = 'sacipc'
    origin = 'za_company'

    def __init__(self, *args, **kwargs):
        super(CompanyAnalyzer, self).__init__(*args, **kwargs)
        self.entities = []
        self.extractor = CompanyExtractor()
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
        if self.disabled or text is None:
            return
        for company in self.extractor.on_text(text):
            self.entities.append((company.regno, company.name, company.fullname))

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
