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
                ('1999/005161/07',
                 'Gauteng Enclosure Manufacturers (Pty)',
                 'Gauteng Enclosure Manufacturers (Pty) (Reg. No. 1999/005161/07)'),
                ('1991/004341/07',
                 'Venue Finders (Pty) Ltd',
                 'Venue Finders (Pty) Ltd (Reg. No. 1991/004341/07)'),
                ('1995/010219/07',
                 'Phakamani Warehousing and Distribution Services (Pty)',
                 'Phakamani Warehousing and Distribution Services (Pty) (Reg. No. 1995/010219/07)')
            ]
            for e in expected:
                assert e in a.entities, (e, a.entities)
            assert len(a.entities) == len(expected), (len(a.entities), a.entities)

    def test_companies2(self):
        with open(os.path.join(FIXTURES, 'companies_02.txt')) as f:
            text = f.read()
            a = Company(None, None)
            a.on_text(text)
            expected = [
                ('2010/080078/23',
                 'Blissful Insight Trading 15 CC t/a Tyrenet Kuils Rivier',
                 'Blissful Insight Trading 15 CC t/a Tyrenet Kuils Rivier (Reg. No. 2010/080078/23)'),
                ('2011/007918/07',
                 'Topassist 41 (Pty)',
                 'Topassist 41 (Pty) (Reg. No. 2011/007918/07)'),
                ('2005/041610/23',
                 'Silver Moon Investments 166 CC',
                 'Silver Moon Investments 166 CC (Reg. No. 2005/041610/23)'),
                ('2006/153590/23',
                 'Ethos Logostics CC',
                 'Ethos Logostics CC (Reg. No. 2006/153590/23)'),
                ('2006/169475/23',
                 'Bay Bottlers CC',
                 'Bay Bottlers CC (Reg. No. 2006/169475/23)'),
                ('2005/006753/23',
                 'Wilcon Construction',
                 'Wilcon Construction (Reg. No. 2005/006753/23)'),
                ('2004/009825/07',
                 'Admirals',
                 'Admirals (Reg. No. 2004/009825/07)'),
                ('2006/219181/23',
                 'Speedfit Jeffreys Bay',
                 'Speedfit Jeffreys Bay (Reg. No. 2006/219181/23)'),
                ('2009/030703/23',
                 'Setlhapelo Trading Enterprises CC',
                 'Setlhapelo Trading Enterprises CC (Reg. No. 2009/030703/23)'),
                ('2008/005237/07',
                 'Limited',
                 'Limited (Reg. No. 2008/005237/07)'),
                ('2005/023479/07',
                 'Ltd',
                 'Ltd (Reg. No. 2005/023479/07)'),
                ('2009/056825/23',
                 'DRM Automotive CC',
                 'DRM Automotive CC (Reg. No. 2009/056825/23)'),
                ('2001/049541/23',
                 'Cormeg Projects CC',
                 'Cormeg Projects CC (Reg. No. 2001/049541/23)'),
                ('1998/041813/23',
                 'CC',
                 'CC (Reg. No. 1998/041813/23)'),
                ('2013/0235598/07',
                 'Synergy Auto Sales (Pty) Ltd',
                 'Synergy Auto Sales (Pty) Ltd (Reg. No. 2013/0235598/07)'),
                ('1990/034742/23',
                 'Mackay Bridge Farm CC',
                 'Mackay Bridge Farm CC (Reg. No. 1990/034742/23)')
            ]
            for e in expected:
                assert e in a.entities, (e, a.entities)
                assert len(a.entities) == len(expected), (len(a.entities), a.entities)
                
