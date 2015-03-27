# coding=utf-8
import unittest
from django.conf import settings
settings.configure()

from mangashost.pages_parser import PagesParser


class PagesParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = PagesParser()

    def test_can_fetch_chapter_page(self):
        pages = self.parser.parse_chapters_pages(u"http://br.mangahost.com/manga/one-piece-pt-br/1")
        self.assertTrue(len(pages) == 63,
                        u"One Piece first chapters page number didn't match, expected 63, got {}".format(len(pages)))

    def test_can_fetch_custom_chapter_page(self):
        pages = self.parser.parse_chapters_pages(u"http://br.mangahost.com/manga/bleach-pt-br/1")
        self.assertTrue(len(pages) == 56,
                        u"Bleach first chapters page number didn't match, expected 56, got {}".format(len(pages)))