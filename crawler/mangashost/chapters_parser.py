import re

from bs4 import BeautifulSoup


class CommonChapterParser(object):
    def should_parse(self, soup):
        return soup.find("a", class_="capitulo") is not None

    def parse(self, soup, url):
        chapter_links = soup.find_all('a', class_="capitulo", href=re.compile(r'.*/manga/.*'))
        return [{'url': a['href'], 'name': a.text} for a in chapter_links]


class CustomPageChapterParser(object):
    def should_parse(self, soup):
        return soup.find("ul", class_="list_chapters") is not None

    def parse(self, soup, url):
        chapters_container = soup.find('ul', class_="list_chapters")
        chapters_link = chapters_container.find_all('a', {"data-html": "true"})
        chapters = []

        for link in chapters_link:
            inner_html = BeautifulSoup(link['data-content'], 'lxml')
            a = inner_html.find('a')
            chapters.append({'url': a['href'], 'name': a.text})

        return chapters


available_chapter_parsers = (CommonChapterParser(), CustomPageChapterParser())