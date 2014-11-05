import re

from bs4 import BeautifulSoup

from crawler.utils import get_html


class CommonChapterParser(object):
    BASE_URL = "http://centraldemangas.net{}"

    def should_parse(self, url):
        return "centraldemangas.net" in url

    def parse(self, soup, url):
        chapter_links = soup.find_all('a', href=re.compile(r'.*/online/.*'))
        return [{'url': self.BASE_URL.format(a['href']), 'name': a.text} for a in chapter_links]


class CustomPageChapterParser(object):
    def should_parse(self, url):
        return "centraldemangas.net" not in url

    def parse(self, soup, url):
        raw_url = url.replace("/informacoes/sinopse", "")
        list_pages = self.get_all_chapter_pages(raw_url)
        chapters = []

        for page in list_pages:
            chapters.extend(self.get_chapters_in_page(page))

        return chapters

    @staticmethod
    def get_all_chapter_pages(base_url):
        html, _ = get_html(base_url + "/capitulos")
        soup = BeautifulSoup(html, 'lxml')
        pagination_links = soup.find('ul', class_='pagination').find_all('a', href=re.compile(r'.*/capitulos\?page=\d*'))
        return [base_url + a['href'] for a in pagination_links]

    @staticmethod
    def get_chapters_in_page(url):
        raw_url = url.rsplit('/', 1)[0]
        html, _ = get_html(url)
        chapter_soup = BeautifulSoup(html, 'lxml')
        chapter_links = chapter_soup.find('table', class_='table').find_all('a', href=re.compile(r'.*/online/.*'))
        return [{'url': raw_url + a['href'], 'name': a.text} for a in chapter_links]


available_chapter_parsers = (CommonChapterParser(), CustomPageChapterParser())