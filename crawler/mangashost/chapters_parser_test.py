# coding=utf-8
import unittest
from django.conf import settings
settings.configure()

from bs4 import BeautifulSoup

from crawler.utils import get_html
from mangashost.chapters_parser import CommonChapterParser, CustomPageChapterParser
from mangashost.index_parser import IndexParser


class CommonChapterParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = CommonChapterParser()

    def test_can_fetch_manga_chapters(self):
        url = "http://br.mangahost.com/manga/07-ghost"
        html, _ = get_html(url, IndexParser.HEADERS)
        soup = BeautifulSoup(html, 'lxml')
        self.assertTrue(len(self.parser.parse(soup, url)) >= 47, u"Cannot get chapter pages from mangás host...")

    def test_can_fetch_only_cdm_chapters(self):

        html, _ = get_html("http://br.mangahost.com/manga/07-ghost", IndexParser.HEADERS)
        soup = BeautifulSoup(html, 'lxml')
        self.assertTrue(self.parser.should_parse(soup))

        html, _ = get_html('http://br.mangahost.com/manga/gantz', IndexParser.HEADERS)
        soup = BeautifulSoup(html, 'lxml')
        self.assertFalse(self.parser.should_parse(soup))


class CustomPageChapterParserTest(unittest.TestCase):
    def setUp(self):
        self.parser = CustomPageChapterParser()

    def test_can_fetch_manga_chapters(self):
        url = "http://br.mangahost.com/manga/gantz"
        html, _ = get_html(url, IndexParser.HEADERS)
        soup = BeautifulSoup(html, 'lxml')
        self.assertTrue(len(self.parser.parse(soup, url)) == 383, u"Cannot get chapter pages from mangás host...")

    def test_can_fetch_only_cdm_chapters(self):
        html, _ = get_html("http://br.mangahost.com/manga/07-ghost", IndexParser.HEADERS)
        soup = BeautifulSoup(html, 'lxml')
        self.assertFalse(self.parser.should_parse(soup))

        html, _ = get_html('http://br.mangahost.com/manga/gantz', IndexParser.HEADERS)
        soup = BeautifulSoup(html, 'lxml')
        self.assertTrue(self.parser.should_parse(soup))
