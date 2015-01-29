import urllib2
from difflib import SequenceMatcher


def is_similar(a, b, rating=0.5):
    return SequenceMatcher(None, a, b).ratio() > rating


def get_html(url, header={}):
    req = urllib2.Request(url)
    for k, v in header.items():
        req.add_header(k, v)

    url_open = urllib2.urlopen(req, timeout=60)
    html = url_open.read()
    url_open.close()
    return html, url_open.url