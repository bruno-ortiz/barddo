# coding=utf-8
import unittest
from centraldemangas.index_parser import IndexParser


class IndexParserTest(unittest.TestCase):

    def setUp(self):
        self.parser = IndexParser()

    def test_can_fetch_all_pages(self):
        self.assertTrue(len(self.parser.get_all_pages()) > 40, u"Cannot get paginated pages from central de mangás...")

    def test_can_fetch_mangas_in_page(self):
        results = self.parser.get_mangas_in_page("/mangas/list/*/1")
        self.assertTrue(len(results) == 30, u"First page listing didn't return 30 itens... Please check!")
