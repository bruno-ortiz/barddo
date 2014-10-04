# coding=utf-8
from os.path import expanduser
import urllib2
import re
import pickle

from bs4 import BeautifulSoup


BASE_URL = "http://centraldemangas.net{}"

INITIAL_URL = BASE_URL.format("/mangas/list/*")


def __should_parse(url):
    return 'informacoes/sinopse' not in url


def __get_html(url):
    url_open = urllib2.urlopen(url)
    html = url_open.read()
    url_open.close()
    return html


def __get_manga_pages(soup):
    pagination_links = soup.find('ul', class_='pagination').find_all('a', href=re.compile(r'.*/mangas/list/*/.*'))
    pagination_urls = [a['href'] for a in pagination_links]
    manga_urls = []
    for page_url in pagination_urls:
        url = BASE_URL.format(page_url)
        html = __get_html(url)
        manga_soup = BeautifulSoup(html, 'lxml')
        manga_links = manga_soup.find('table', class_='table').find_all('a', href=re.compile(r".*/mangas/info/.*"))
        url_list = [a['href'] for a in manga_links]
        manga_urls.extend(url_list)
    return manga_urls


def __author_name(soup):
    try:
        author = soup.find('h4', text='Autor').find_parent('div', class_='row').find_next_sibling('div').findChild('a').text
    except Exception as e:
        print 'Falha ao obter nome do author. Erro: {}'.format(str(e))
        author = 'Desconhecido'
    return author


def __tags(soup):
    try:
        tags_links = soup.find('h4', text='Gênero').find_parent('div', class_='row').find_next_sibling('div').findChildren('a')
        tags = [a.text for a in tags_links]
    except Exception as e:
        print 'Falha ao obter tags. Erro: {}'.format(str(e))
        tags = ['Desconhecido']
    return tags


def __status(soup):
    try:
        status = soup.find('h4', text='Status').find_parent('div', class_='row').find_next_sibling('div').findChild('a').text
    except Exception as e:
        print 'Falha ao obter status. Erro: {}'.format(str(e))
        status = 'Desconhecido'
    return status


def __sinopse(soup):
    try:
        sinopse = soup.find('p').text
    except Exception as e:
        print 'Falha ao obter sinopse. Erro: {}'.format(str(e))
        sinopse = 'Sem sinopse'
    return sinopse


def __parse_chapters(soup):
    try:
        chapter_links = soup.find_all('a', href=re.compile(r'.*/online/.*'))
        chapter_list = [{'url': a['href'], 'name': a.text} for a in chapter_links]
        for chapter in chapter_list:
            url = BASE_URL.format(chapter['url'])
            html = __get_html(url)
            r = re.compile(r'.*var\spages.*\[(.*)\]')
            if r.search(html):
                print 'Obtendo páginas do capitulos {}'.format(chapter['name'])
                raw_pages = r.search(html).group(1)
                pages = raw_pages.replace('\\', '').replace('"', '').split(',')
            else:
                pages = []
            chapter['pages'] = pages
    except Exception as e:
        print 'Falha ao obter capitulos. Erro: {}'.format(str(e))
        chapter_list = []
    return chapter_list


def __extract_manga_data(url):
    html = __get_html(url)
    soup = BeautifulSoup(html, 'lxml')
    cover = soup.find('div', class_="pull-left").find('img', class_='img-thumbnail')['src']
    name = soup.find('div', class_='page-header').find('h1').contents[0].strip()
    print 'Obtendo dados de: {}'.format(name)
    author = __author_name(soup)
    tags = __tags(soup)
    status = __status(soup)
    sinopse = __sinopse(soup)
    chapters = __parse_chapters(soup)
    data = {'cover': cover,
            'author': author,
            'tags': tags,
            'status': status,
            'sinopse': sinopse,
            'chapters': chapters}
    return name, data


def __count_data(data):
    chapter_count = 0
    page_count = 0
    for d in data:
        chapters = d['chapters']
        chapter_count += len(chapters)
        for c in chapters:
            p = c['pages']
            page_count += len(p)
    print 'Capitulos: {}'.format(chapter_count)
    print 'Páginas: {}'.format(page_count)


def extract_data():
    html = __get_html(INITIAL_URL)
    soup = BeautifulSoup(html, 'lxml')
    all_pages = __get_manga_pages(soup)
    data = {}
    for page in all_pages:
        url = BASE_URL.format(page)
        if __should_parse(url):
            name, manga_data = __extract_manga_data(url)
            data[name] = manga_data
    data_file = expanduser("~") + '/mangas.pickle'
    with open(data_file, 'wb') as handle:
        pickle.dump(data, handle)
    __count_data(data)
    return data


def execute(data_file=None):
    if data_file:
        with open(data_file, 'rb') as handle:
            data = pickle.load(handle)
    else:
        data = extract_data()
    return data
