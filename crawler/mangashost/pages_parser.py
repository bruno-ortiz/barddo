# coding=utf-8
import re

from crawler.utils import get_html
from mangashost.index_parser import IndexParser
import json
from colorama import Fore


class PagesParser(object):
    def parse_chapters_pages(self, complete_url):
        try:
            html, _ = get_html(complete_url, IndexParser.HEADERS)
            r = re.compile(r'.*var\s+pages\s+=\s+(.*);')
            if r.search(html):
                raw_pages = r.search(html).group(1).replace("}\s*,\s*]", "}]")
                pages_dict = json.loads(raw_pages)
                pages = [d["url"] for d in pages_dict]
            else:
                pages = []
            return pages
        except Exception as e:
            print Fore.RED + u'Falha ao obter páginas de capitulos de "{}". Erro: {}'.format(complete_url, str(e)) + Fore.WHITE
            return []
