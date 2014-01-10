import gzip
from urllib import request
from io import BytesIO
from datetime import datetime


def timestamp2datetime(timestamp):
    return datetime.fromtimestamp(timestamp / 1000.0)


def read_url(url):
    opener = request.build_opener()
    opener.addheaders = [
        ('User-Agent', 'android'),
        ('Referer', 'http://music.163.com/'),
        ('Accept-Encoding', 'gzip'),
    ]

    resp = opener.open(url, timeout=3)
    content = resp.read()
    if resp.headers.get('content-encoding', None) == 'gzip':
        content = gzip.GzipFile(fileobj=BytesIO(content),
                                mode='rb').read().decode('UTF-8')
    return content
