#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gzip
import urllib2
import StringIO
from datetime import datetime

def timestamp2datetime(timestamp):
    return datetime.fromtimestamp(timestamp / 1000.0)

def read_url(url):
    opener = urllib2.build_opener()
    opener.addheaders = [
        ('User-Agent', 'android'),
        ('Referer', 'http://music.163.com/'),
        ('Accept-Encoding', 'gzip'),
    ]

    resp = opener.open(url, timeout=3)
    content = resp.read()
    if resp.headers.get('content-encoding', None) == 'gzip':
        content = gzip.GzipFile(fileobj=StringIO.StringIO(content),
                                mode='rb').read()
    return content
