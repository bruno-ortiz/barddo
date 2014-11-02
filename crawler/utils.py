import urllib2


def get_html(url):
    url_open = urllib2.urlopen(url, timeout=30)
    html = url_open.read()
    url_open.close()
    return html, url_open.url