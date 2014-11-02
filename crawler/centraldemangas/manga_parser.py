# coding=utf-8
import re
from bs4 import BeautifulSoup
from centraldemangas.chapters_parser import available_chapter_parsers
from utils import get_html


class MangaParser(object):

    def extract_manga_data(self, url):
        html, real_url = get_html(url)
        soup = BeautifulSoup(html, 'lxml')
        cover = soup.find('div', class_="pull-left").find('img', class_='img-thumbnail')['src']
        name = soup.find('div', class_='page-header').find('h1').contents[0].strip()

        print 'Obtendo dados de: {}'.format(name)
        author = self.__author_name(soup)
        tags = self.__tags(soup)
        status = self.__status(soup)
        sinopse = self.__summary(soup)
        chapters = None

        for parser in available_chapter_parsers:
            if parser.should_parse(real_url):
                chapters = parser.parse(soup, real_url)
                break

        if not chapters:
            chapters = []
            #raise RuntimeError("Cannot find a valid chapters parser for {}".format(real_url))

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
            author = soup.find('h4', text='Autor').find_parent('div', class_='row').find_next_sibling('div').findChild('a').text
        except Exception as e:
            print 'Falha ao obter nome do author. Erro: {}'.format(str(e))
            author = 'Desconhecido'
        return author

    @staticmethod
    def __tags(soup):
        try:
            tags_links = soup.find('h4', text='Gênero').find_parent('div', class_='row').find_next_sibling('div').findChildren('a')
            tags = [a.text for a in tags_links]
        except Exception as e:
            print 'Falha ao obter tags. Erro: {}'.format(str(e))
            tags = ['Desconhecido']
        return tags


    @staticmethod
    def __status(soup):
        try:
            status = soup.find('h4', text='Status').find_parent('div', class_='row').find_next_sibling('div').findChild('a').text
        except Exception as e:
            print 'Falha ao obter status. Erro: {}'.format(str(e))
            status = 'Desconhecido'
        return status

    @staticmethod
    def __summary(soup):
        try:
            sinopse = soup.find('p').text
            if not sinopse:
                sinopse = soup.find('p').find_next_sibling('div').text
        except Exception as e:
            print 'Falha ao obter sinopse. Erro: {}'.format(str(e))
            sinopse = 'Sem sinopse'
        else:
            if not sinopse:
                sinopse = u'Sem descrição'
        return sinopse