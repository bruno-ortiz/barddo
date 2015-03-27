# coding=utf-8
import unittest
from django.conf import settings
settings.configure()


from crawler.centraldemangas.pages_parser import PagesParser


class PagesParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = PagesParser()

    def test_can_fetch_chapter_page(self):
        pages = self.parser.parse_chapters_pages(u"http://centraldemangas.net/online/one-piece/001")
        self.assertTrue(len(pages) == 63,
                        u"One Piece first chapters page number didn't match, expected 63, got {}".format(len(pages)))

    def test_can_fetch_custom_chapter_page(self):
        pages = self.parser.parse_chapters_pages(u"http://bleachmanga.com.br/leitura/online/capitulo/001")
        self.assertTrue(len(pages) == 55,
                        u"Bleach first chapters page number didn't match, expected 55, got {}".format(len(pages)))