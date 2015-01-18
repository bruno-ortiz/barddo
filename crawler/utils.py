import urllib2


def get_html(url, header={}):
    req = urllib2.Request(url)
    for k, v in header.items():
        req.add_header(k, v)

    url_open = urllib2.urlopen(req, timeout=30)
    html = url_open.read()
    url_open.close()
    return html, url_open.url