from aleph_za_entities import Company
from unittest import TestCase


class EntitiesTestCase(TestCase):

    def test_on_text_empty(self):
        analyser = Company()
        analyser.on_text('')
        assert analyser.entities == []
