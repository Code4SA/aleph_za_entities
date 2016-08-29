from aleph_za_entities.companies import Company
from aleph_za_entities.sa_ids import Persons
import os

FIXTURES = os.path.join(os.path.dirname(__file__), 'fixtures')


def test_on_text_empty():
    a = Company(None, None)
    a.on_text('')
    assert a.entities == [], a.entities

def test_companies():
    with open(os.path.join(FIXTURES, 'entities_01.txt')) as f:
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
            yield check_entity_tuple, a.entities, e
        assert len(a.entities) == len(expected), (len(a.entities), a.entities)

def test_companies2():
    """
    - freestanding numbers
    - t/a
    - multiple spaces anywhere
    """
    with open(os.path.join(FIXTURES, 'entities_02.txt')) as f:
        text = f.read()
        a = Company(None, None)
        a.on_text(text)
        expected = [
            ('2010/080078/23',
             'Blissful Insight Trading 15 CC t/a Tyrenet Kuils Rivier',
             'Blissful Insight Trading 15 CC t/a Tyrenet Kuils Rivier (Reg. No. 2010/080078/23)'),
            ('2011/007918/07',
             'Topassist 41 (Pty) Ltd',
             'Topassist 41 (Pty) Ltd (Reg. No. 2011/007918/07)'),
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
             'William Van Heerden Construction t/a Wilcon Construction',
             'William Van Heerden Construction t/a Wilcon Construction (Reg. No. 2005/006753/23)'),
            ('2004/009825/07',
             'Caveman Bites (Pty) Ltd t/a Admirals',
             'Caveman Bites (Pty) Ltd t/a Admirals (Reg. No. 2004/009825/07)'),
            ('2006/219181/23',
             'Merlico 139 CC t/a Speedfit Jeffreys Bay',
             'Merlico 139 CC t/a Speedfit Jeffreys Bay (Reg. No. 2006/219181/23)'),
            ('2009/030703/23',
             'Setlhapelo Trading Enterprises CC',
             'Setlhapelo Trading Enterprises CC (Reg. No. 2009/030703/23)'),
            ('2008/005237/07',
             'Shelfzone 119 (Pty) Limited',
             'Shelfzone 119 (Pty) Limited (Reg. No. 2008/005237/07)'),
            ('2005/023479/07',
             'Sapphire Cove Investments 16 (Pty) Ltd',
             'Sapphire Cove Investments 16 (Pty) Ltd (Reg. No. 2005/023479/07)'),
            ('2009/056825/23',
             'DRM Automotive CC',
             'DRM Automotive CC (Reg. No. 2009/056825/23)'),
            ('2001/049541/23',
             'Cormeg Projects CC',
             'Cormeg Projects CC (Reg. No. 2001/049541/23)'),
            ('1998/041813/23',
             'Dandyshelf 1007 CC',
             'Dandyshelf 1007 CC (Reg. No. 1998/041813/23)'),
            ('2013/0235598/07',
             'Synergy Auto Sales (Pty) Ltd',
             'Synergy Auto Sales (Pty) Ltd (Reg. No. 2013/0235598/07)'),
            ('1990/034742/23',
             'Mackay Bridge Farm CC',
             'Mackay Bridge Farm CC (Reg. No. 1990/034742/23)')
        ]
        for e in expected:
            yield check_entity_tuple, a.entities, e
            assert len(a.entities) == len(expected), (len(a.entities), a.entities)


def test_sa_nids():
    with open(os.path.join(FIXTURES, 'entities_01.txt')) as f:
        text = f.read()
        a = Persons(None, None)
        a.on_text(text)
        expected = [
            ('7910300007088',
             'Chantel Els',
             'Chantel Els, 7910300007088'),
            ('7705125087087',
             'Willem Jacobus van der Merwe',
             'Willem Jacobus van der Merwe, 7705125087087'),
            ('6311305047081',
             'Graham Ronald Charles',
             'Graham Ronald Charles, 6311305047081'),
            ('7511250160081',
             'Michelle Monique Gardiner',
             'Michelle Monique Gardiner, 7511250160081'),
            ('4910215609088',
             'Molwele Molahlegi Simon',
             'Molwele Molahlegi Simon, 4910215609088'),
            ('8112300139081',
             'Alicia Ann van Putten',
             'Alicia Ann van Putten, 8112300139081'),
            ('8407205089088',
             'Bell Reinhardt',
             'Bell Reinhardt, 8407205089088'),
            ('7404095080088',
             'Graham Paul Schultz',
             'Graham Paul Schultz, 7404095080088'),
            ('8308250675088',
             'Nonhlanhla Mbalenhle Mthethwa',
             'Nonhlanhla Mbalenhle Mthethwa, 8308250675088'),
            ('8107170183086',
             'Susara Johanna Magrieta Booysen',
             'Susara Johanna Magrieta Booysen, 8107170183086'),
            ('8108185049080',
             'Marcus Cilliers',
             'Marcus Cilliers, 8108185049080'),
            ('8208190669086',
             'Gloria Modiegi Pelle',
             'Gloria Modiegi Pelle, 8208190669086'),
            ('8403185602081',
             'Mashudu Wayne Mandiwana',
             'Mashudu Wayne Mandiwana, 8403185602081'),
            ('6403065107088',
             'Nicolaas Jacob Badenhorst',
             'Nicolaas Jacob Badenhorst, 6403065107088'),
            ('8409020290081',
             'Shernel Mouton',
             'Shernel Mouton, 8409020290081'),
            ('7312165089089',
             'Lion Schalk Postma',
             'Lion Schalk Postma, 7312165089089'),
            ('7802065153088',
             'Johannes Jacobus de Kock',
             'Johannes Jacobus de Kock, 7802065153088'),
            ('7707250018085',
             'Tryna van Wyngaardt-Schoeman',
             'Tryna van Wyngaardt-Schoeman, 7707250018085'),
            ('6201080130089',
             'Annelie Carlo Viviers',
             'Annelie Carlo Viviers, 6201080130089'),
        ]
        for e in expected:
            yield check_entity_tuple, a.entities, e
        assert len(a.entities) == len(expected), (len(a.entities), a.entities)


def check_entity_tuple(entities, entity_tuple):
    assert entity_tuple in entities
