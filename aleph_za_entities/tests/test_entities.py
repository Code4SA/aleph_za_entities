from aleph_za_entities.entities import Company
from unittest import TestCase
import os

FIXTURES = os.path.join(os.path.dirname(__file__), 'fixtures')


class EntitiesTestCase(TestCase):

    def test_on_text_empty(self):
        a = Company(None, None)
        a.on_text('')
        assert a.entities == [], a.entities

    def test_companies(self):
        with open(os.path.join(FIXTURES, 'companies_01.txt')) as f:
            text = f.read()
            a = Company(None, None)
            a.on_text(text)
            expected = [
                ('1968/007463/07',
                 'Mawenzi Asset Managers (Pty) Ltd',
                 'Mawenzi Asset Managers (Pty) Ltd (Reg. No. 1968/007463/07)'),
                ('1995/010219/07',
                 'Distribution Services (Pty)',
                 'Distribution Services (Pty) (Reg. No. 1995/010219/07)')
            ]
            for e in expected:
                assert e in a.entities, e
