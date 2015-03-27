import re
import os

from bs4 import BeautifulSoup

from crawler.utils import get_html


class IndexParser(object):
    BASE_URL = "http://br.mangahost.com{}"

    INITIAL_URL = BASE_URL.format("/mangas")

    PAGINATED_URL = BASE_URL.format("/mangas/page/{}")

    HEADERS = {
        "Referer": "http://br.mangahost.com/",
        "User-Agent": "Mozilla/5.0"
    }

    def get_manga_list(self):
        base_path = os.path.dirname(__file__)
        file_path = os.path.join(base_path, "mangas_list.txt")

        with open(file_path) as mangas_list:
            return mangas_list.readlines()

    def get_all_pages(self):
        html, _ = get_html(self.INITIAL_URL, self.HEADERS)
        soup = BeautifulSoup(html, 'lxml')
        last_page_link = soup.find('div', class_='wp-pagenavi').find('a', class_="last")['href']
        last_page_number = int(last_page_link.split('/')[-1])
        return [self.PAGINATED_URL.format(n) for n in xrange(1, last_page_number + 1)]

    def get_mangas_in_page(self, url):
        html, _ = get_html(url, self.HEADERS)
        manga_soup = BeautifulSoup(html, 'lxml')
        manga_links = manga_soup.find('div', class_='list').find_all('a', href=re.compile(
            r".*br\.mangahost\.com/manga/.*"))
        return set([a['href'] for a in manga_links])

    @staticmethod
    def should_parse(url):
        return 'informacoes/sinopse' not in url