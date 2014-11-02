import re
from bs4 import BeautifulSoup
from utils import get_html


class IndexParser(object):

    BASE_URL = "http://centraldemangas.net{}"

    INITIAL_URL = BASE_URL.format("/mangas/list/*")

    def get_manga_list(self):
        manga_urls = []
        for relative_url in self.get_all_pages():
            manga_urls.extend(self.get_mangas_in_page(relative_url))
        return [self.BASE_URL.format(url) for url in manga_urls if self.should_parse(url)]

    def get_all_pages(self):
        html, _ = get_html(self.INITIAL_URL)
        soup = BeautifulSoup(html, 'lxml')
        pagination_links = soup.find('ul', class_='pagination').find_all('a', href=re.compile(r'.*/mangas/list/*/.*'))
        return [a['href'] for a in pagination_links]

    def get_mangas_in_page(self, relative_url):
        url = self.BASE_URL.format(relative_url)
        html, _ = get_html(url)
        manga_soup = BeautifulSoup(html, 'lxml')
        manga_links = manga_soup.find('table', class_='table').find_all('a', href=re.compile(r".*/mangas/info/.*"))
        return [a['href'] for a in manga_links]

    @staticmethod
    def should_parse(url):
        return 'informacoes/sinopse' not in url