# coding=utf-8
import re

from crawler.utils import get_html
from mangashost.index_parser import IndexParser
import json

class PagesParser(object):
    def parse_chapters_pages(self, complete_url):
        try:
            html, _ = get_html(complete_url, IndexParser.HEADERS)
            'http:\/\/img.mangahost.com\/br\/images\/bleach-pt-br\/611\/00.png'
            r = re.compile(r'.*var\spages.*(\[.*\])')
            if r.search(html):
                raw_pages = r.search(html).group(1)
                pages_dict = json.loads(raw_pages)
                pages = [d["url"] for d in pages_dict]
            else:
                pages = []
            return pages
        except Exception as e:
            print u'Falha ao obter páginas de capitulos. Erro: {}'.format(str(e))
            return []
