# coding=utf-8
import unittest
from mangashost.index_parser import IndexParser


class IndexParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = IndexParser()

    def test_can_fetch_all_pages(self):
        self.assertTrue(len(self.parser.get_all_pages()) >= 68, u"Cannot get paginated pages from mangás host...")

    def test_can_fetch_mangas_in_page(self):
        results = self.parser.get_mangas_in_page("http://br.mangahost.com/mangas/page/1")
        self.assertTrue(len(results) == 42, u"First page listing didn't return 42 itens... Please check!")
