from lxml import etree


BASE_URL = "http://centraldemangas.net{}"

INITIAL_URL = BASE_URL.format("/mangas/list/*")


def __get_manga_pages(parsed):
    pagination_urls = parsed.xpath('//a[contains(@href,"/mangas/list/*/")]/@href')
    manga_urls = []
    for page_url in pagination_urls:
        url = BASE_URL.format(page_url)
        url_list = etree.parse(url, etree.HTMLParser()).xpath('//table//a[contains(@href,"/mangas/info/")]/@href')
        manga_urls.extend(url_list)
    return manga_urls


def __extract_manga_data(page):
    url = BASE_URL.format(page)
    parsed_page = etree.parse(url, etree.HTMLParser())
    (cover,) = parsed_page.xpath('//div[@class="pull-left"]/img[@class="img-thumbnail"]/@src')
    name = parsed_page.xpath('//div[@class="page-header"]/h1/text()')[0].strip()
    data = {'name': name, 'cover': cover}
    return data


def extract_data():
    parsed = etree.parse(INITIAL_URL, etree.HTMLParser())
    all_pages = __get_manga_pages(parsed)
    data = []
    for page in all_pages:
        manga_data = __extract_manga_data(page)
        data.append(manga_data)
    return data


if __name__ == '__main__':
    extract_data()