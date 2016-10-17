# -*- coding: utf-8 -*-

from aleph_za_entities.companies import CompanyExtractor
from aleph_za_entities.sa_ids import Persons
import os

FIXTURES = os.path.join(os.path.dirname(__file__), 'fixtures')


def test_on_text_empty():
    ex = CompanyExtractor()
    entities = ex.on_text('')
    assert entities == [], entities


def test_companies():
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
    with open(os.path.join(FIXTURES, 'entities_01.txt')) as f:
        text = f.read()
        ex = CompanyExtractor()
        entities = ex.on_text(text)
    for e in expected:
        yield check_company_tuple, entities, e
    yield check_expected_actual_length, expected, entities


def test_companies2():
    """
    - freestanding numbers
    - t/a
    - multiple spaces anywhere
    """
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
    with open(os.path.join(FIXTURES, 'entities_02.txt')) as f:
        text = f.read()
        ex = CompanyExtractor()
        entities = ex.on_text(text)
    for e in expected:
        yield check_company_tuple, entities, e
    yield check_expected_actual_length, expected, entities


def test_companies3():
    """
    - names that were incorrectly extracted as single-word names
    - ignore things with domain-specific labels between name and reg nr
    - ignore reg nr not in parens otherwise we might open a can of worms
    - ignore reg nr in parens without "Reg No" in some form prefixing it inside
      parens for same reason
    - ignore single-word names which has nice effect of ignoring addresses in the
      usual position of the name where the postal region is one word
      (in this case "LYTTELTON MANOR, PRETORIA (Registrasie No. 2006/017140/07)")
    """
    expected = [
        ('2006/041818/23',
         'Homefront Trading 26CC',
         'Homefront Trading 26CC (Reg. No. 2006/041818/23)'),
        ('2005/159546/23',
         'Uptown trading 680 CC',
         'Uptown trading 680 CC (Reg. No. 2005/159546/23)'),
        ('2009/023427/23',
         'Olifants River Safari’s CC',
         'Olifants River Safari’s CC (Reg. No. 2009/023427/23)'),
        ('2009/023427/23',
         'Olifants River Safari’s BK',
         'Olifants River Safari’s BK (Reg. No. 2009/023427/23)'),
        ('2006/134568/23',
         'Teak From Africa CC',
         'Teak From Africa CC (Reg No. 2006/134568/23)'),
        ('2006/134568/23',
         'Teak From Africa CC',
         'Teak From Africa CC (Reg. No. 2006/134568/23)'),
        ('2006/134568/23',
         'TEAK FROM AFRICA CC',
         'TEAK FROM AFRICA CC (Reg. No. 2006/134568/23)'),
        ('2006/134568/23',
         'Teak From Africa',
         'Teak From Africa (Reg. No. 2006/134568/23)'),
        ('2006/134568/23',
         'Teak From Africa',
         'Teak From Africa (Reg. No. 2006/134568/23)'),
        ('2008/018264/07',
         'R Estate Café CC',
         'R Estate Café CC (Reg No. 2008/018264/07)'),
        ('2006/017140/07',
         'Revolution Business Solutions (Edms) Bpk',
         'Revolution Business Solutions (Edms) Bpk (Reg. No. 2006/017140/07)'),
        ('2010/135710/23',
         'Go Club at 925 CC',
         'Go Club at 925 CC (Reg. No. 2010/135710/23)'),
        ('2010/115894/23',
         'Riebeeck Vallei Drankwinkel CC',
         'Riebeeck Vallei Drankwinkel CC (Reg. No. 2010/115894/23)'),
        ('2008/038059/23',
         'Professional Mechanical services CC',
         'Professional Mechanical services CC (Reg. No. 2008/038059/23)'),
    ]
    with open(os.path.join(FIXTURES, 'entities_04_companies_not_single_word.txt')) as f:
        text = f.read()
        ex = CompanyExtractor()
        entities = ex.on_text(text)
    for e in expected:
        yield check_company_tuple, entities, e
    yield check_expected_actual_length, expected, entities


def test_sa_nids():
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
        ('7707250018085',
         'Tryna van Wyngaardt-Schoeman',
         'Tryna van Wyngaardt-Schoeman, 7707250018085'),
        ('6201080130089',
         'Annelie Carlo Viviers',
         'Annelie Carlo Viviers, 6201080130089'),
    ]
    with open(os.path.join(FIXTURES, 'entities_01.txt')) as f:
        text = f.read()
        a = Persons(None, None)
        a.on_text(text)
    for e in expected:
        yield check_said_tuple, a.entities, e
    yield check_expected_actual_length, expected, a.entities


def test_sa_nids2():
    expected = [
        ('6112165044089',
         'Khan, Shabeer',
         'Khan, Shabeer, 6112165044089'),
        ('6405310169086',
         'Rookshana Banoo Khan',
         'Rookshana Banoo Khan, 6405310169086'),
        ('3902025599089',
         'Gcwabaza, Jabulani Alfred',
         'Gcwabaza, Jabulani Alfred, 3902025599089'),
        ('4912160909083',
         'Duduzile Winefred Gcwabaza',
         'Duduzile Winefred Gcwabaza, 4912160909083'),
        ('2912105065084',
         'Chetty, Sathasivum Verngopaul',
         'Chetty, Sathasivum Verngopaul, 2912105065084'),
        ('3305140196080',
         'Jala Kumari Chetty',
         'Jala Kumari Chetty, 3305140196080'),
        ('2008060004182',
         'Godwin, Mary',
         'Godwin, Mary, 2008060004182'),
        ('2308140138087',
         'Gwala, Francina',
         'Gwala, Francina, 2308140138087'),
        ('2909130002181',
         'McIntyre, Pamela Joyce',
         'McIntyre, Pamela Joyce, 2909130002181'),
        ('6807075551087',
         'Elliot Mbongiseni Ndwandwe',
         'Elliot Mbongiseni Ndwandwe, 6807075551087'),
        ('4401190114088',
         'Perrimal, Angamma',
         'Perrimal, Angamma, 4401190114088'),
        ('4307045051088',
         'Balakrishna Perrimal',
         'Balakrishna Perrimal, 4307045051088'),
        ('3912105130085',
         'Govender, Subramoni',
         'Govender, Subramoni, 3912105130085'),
        ('3706070060081',
         'Ammooammal Govender',
         'Ammooammal Govender, 3706070060081'),
        ('3307185020084',
         'Funk, Harry',
         'Funk, Harry, 3307185020084'),
        ('5007135082089',
         'Van Jaarsvled, Hendrik Johannes',
         'Van Jaarsvled, Hendrik Johannes, 5007135082089'),
        ('5502140012089',
         'Mary-Ann van Jaarsveld',
         'Mary-Ann van Jaarsveld, 5502140012089'),
        ('5612080100081',
         'Yates, Patricia',
         'Yates, Patricia, 5612080100081'),
        ('5807240006083',
         'Frank, Fiona Jane',
         'Frank, Fiona Jane, 5807240006083'),
        ('4501285092089',
         'Mahabir, Nundkumar',
         'Mahabir, Nundkumar, 4501285092089'),
        ('5109040526083',
         'Veena Mahabir',
         'Veena Mahabir, 5109040526083'),
        ('4406010061187',
         'Berry, Dorothy Margaret',
         'Berry, Dorothy Margaret, 4406010061187'),
        ('3912105130085',
         'Govender, Subramoni',
         'Govender, Subramoni, 3912105130085'),
        ('3706070060081',
         'Ammooammal Govender',
         'Ammooammal Govender, 3706070060081'),
        ('2605130001088',
         'Small, Sheila Elizabeth',
         'Small, Sheila Elizabeth, 2605130001088'),
        ('3204290067086',
         'Wentzel, Ruth',
         'Wentzel, Ruth, 3204290067086'),
        ('4907135115089',
         'Ramroop, Sunker',
         'Ramroop, Sunker, 4907135115089'),
        ('2401275009080',
         'Roy Bennion',
         'Roy Bennion, 2401275009080'),
        ('6007275175080',
         'Sader, Hoosen Yusuf',
         'Sader, Hoosen Yusuf, 6007275175080'),
        ('6105170170089',
         'Nazira Parwi Sader',
         'Nazira Parwi Sader, 6105170170089'),
        ('6007275175080',
         'Sader, Hoosen Yusuf',
         'Sader, Hoosen Yusuf, 6007275175080'),
        ('6105170170089',
         'Nazira Parwi Sader',
         'Nazira Parwi Sader, 6105170170089'),
        ('7509145146083',
         'Reddy, Devadasen',
         'Reddy, Devadasen, 7509145146083'),
        ('8209120026082',
         'Kalaimagal, Reddy',
         'Kalaimagal, Reddy, 8209120026082')
    ]
    with open(os.path.join(FIXTURES, 'entities_03.txt')) as f:
        text = f.read()
        a = Persons(None, None)
        a.on_text(text)
    for e in expected:
        yield check_said_tuple, a.entities, e
    yield check_expected_actual_length, expected, a.entities


def test_sa_nids3():
    """
    names that were incorrectly extracted as single words
    - skip when ID in parens instead of following a comma for now (See Juan Pace
    """
    expected = [
        ('3112030024087',
         'Hamman, Johanna Cornelia',
         'Hamman, Johanna Cornelia, 3112030024087'),
        ('7801050277080',
         'SHEILA MUHAMED JOSE',
         'SHEILA MUHAMED JOSE, 7801050277080'),
        ('6607225112081',
         'Williams, Wyne Coad',
         'Williams, Wyne Coad, 6607225112081'),
        ('6702240131081',
         'Francina Hendrina Magdalena le Roux',
         'Francina Hendrina Magdalena le Roux, 6702240131081'),
        ('4012040037088',
         'Le Roux, Frida Sofie',
         'Le Roux, Frida Sofie, 4012040037088'),
        ('3403225033086',
         'Christiaan Benjamin le Roux',
         'Christiaan Benjamin le Roux, 3403225033086'),
    ]
    with open(os.path.join(FIXTURES, 'entities_05_names_not_single_word.txt')) as f:
        text = f.read()
        a = Persons(None, None)
        a.on_text(text)
    for e in expected:
        yield check_said_tuple, a.entities, e
    yield check_expected_actual_length, expected, a.entities


def check_said_tuple(entities, entity_tuple):
    assert entity_tuple in entities, "\n\nExpected: %r\n\nIn actuals: %r" % (entity_tuple, entities)


def check_company_tuple(entities, entity_tuple):
    tuples = [(e.regno, e.name, e.fullname) for e in entities]
    assert entity_tuple in tuples, "\n\nExpected: %r\n\nIn actuals: %r" % (entity_tuple, tuples)


def check_expected_actual_length(expected, actual):
    assert len(actual) == len(expected), "\n\nExpected %d != Actual %d\n\nActual: %r" % (len(expected), len(actual), actual)
