# coding=utf-8
import re

from crawler.utils import get_html


class PagesParser(object):
    def parse_chapters_pages(self, complete_url):
        try:
            html, _ = get_html(complete_url)
            r = re.compile(r'.*var\spages.*\[(.*)\]')
            if r.search(html):
                raw_pages = r.search(html).group(1)
                pages = raw_pages.replace('\\', '').replace('"', '').split(',')
            else:
                pages = []
            return pages
        except Exception as e:
            print u'Falha ao obter páginas de capitulos. Erro: {}'.format(str(e))
            return []
