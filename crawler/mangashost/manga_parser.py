# coding=utf-8
from bs4 import BeautifulSoup

from crawler.utils import get_html
from mangashost.chapters_parser import available_chapter_parsers
from mangashost.index_parser import IndexParser


class MangaParser(object):
    def extract_manga_data(self, url):
        html, real_url = get_html(url, IndexParser.HEADERS)
        soup = BeautifulSoup(html, 'lxml')

        cover = soup.find('div', class_="content").find('img', class_='thumbnail')['src']
        name = soup.find('div', class_='content').find('h1', class_="entry-title").contents[0].strip()

        print 'Obtendo dados de: {}'.format(name)
        author = self.__author_name(soup)
        tags = self.__tags(soup)
        status = self.__status(soup)
        sinopse = self.__summary(soup)
        chapters = None

        for parser in available_chapter_parsers:
            if parser.should_parse(soup):
                chapters = parser.parse(soup, real_url)
                break

        if not chapters:
            chapters = []
            # raise RuntimeError("Cannot find a valid chapters parser for {}".format(real_url))

        data = {'cover': cover,
                'author': author,
                'tags': tags,
                'status': status,
                'sinopse': sinopse,
                'chapters': chapters}

        return name, data

    @staticmethod
    def __author_name(soup):
        try:
            author = soup.find('strong', text='Autor: ').next_sibling
        except Exception as e:
            print 'Falha ao obter nome do author. Erro: {}'.format(str(e))
            author = 'Desconhecido'
        return author

    @staticmethod
    def __tags(soup):
        try:
            tags_links = soup.find('strong', text='Categoria(s): ').parent.findChildren("a")
            tags = [a.text for a in tags_links]
        except Exception as e:
            print 'Falha ao obter tags. Erro: {}'.format(str(e))
            tags = ['Desconhecido']
        return tags


    @staticmethod
    def __status(soup):
        try:
            status = soup.find('strong', text='Status: ').next_sibling
        except Exception as e:
            print 'Falha ao obter status. Erro: {}'.format(str(e))
            status = 'Desconhecido'
        return status

    @staticmethod
    def __summary(soup):
        try:
            sinopse = soup.find('div', id="divSpdInText").text
        except Exception as e:
            print 'Falha ao obter sinopse. Erro: {}'.format(str(e))
            sinopse = 'Sem sinopse'
        else:
            if not sinopse:
                sinopse = u'Sem descrição'
        return sinopse