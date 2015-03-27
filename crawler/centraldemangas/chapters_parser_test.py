# coding=utf-8
import unittest

from django.conf import settings


settings.configure()

from bs4 import BeautifulSoup

from crawler.centraldemangas.chapters_parser import CommonChapterParser, CustomPageChapterParser
from crawler.utils import get_html


class CommonChapterParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = CommonChapterParser()

    def test_can_fetch_manga_chapters(self):
        url = "http://centraldemangas.org/mangas/info/gantz"
        html, _ = get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        self.assertTrue(len(self.parser.parse(soup, url)) > 380, u"Cannot get chapter pages from central de mangás...")

    def test_can_fetch_only_cdm_chapters(self):
        self.assertTrue(self.parser.should_parse("http://centraldemangas.org/mangas/info/gantz"))
        self.assertFalse(self.parser.should_parse("http://bleachmanga.com.br/capitulos?page=1"))


class CustomPageChapterParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = CustomPageChapterParser()

    def test_can_fetch_manga_chapters(self):
        url = "http://bleachmanga.com.br/capitulos?page=1"
        self.assertTrue(len(self.parser.parse(None, url)) > 380, u"Cannot get chapter pages from central de mangás...")

    def test_can_fetch_only_cdm_chapters(self):
        self.assertFalse(self.parser.should_parse("http://centraldemangas.org/mangas/info/gantz"))
        self.assertTrue(self.parser.should_parse("http://bleachmanga.com.br/capitulos?page=1"))