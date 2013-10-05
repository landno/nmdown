#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from time import time
import urllib2

def urlretrieve(remote_url, local_url, reporthook=None):
    opener = urllib2.build_opener()
    opener.addheaders = [
        ('User-Agent', 'stagefright/1.2(proxy)'),
        ('Referer', 'http://music.163.com/api/'),
    ]
    resp = opener.open(remote_url, timeout=3)
    local_file = open(local_url, 'wb')

    total_size = int(resp.headers.get('Content-Length'))
    block_count = 0
    block_size = 8192
    while True:
        data = resp.read(block_size)
        if not data:
            break
        local_file.write(data)
        block_count += 1
        if reporthook is not None:
            reporthook(block_count, block_size, total_size)
    local_file.flush()
    local_file.close()
    return (local_url, resp.headers.items())

def create_process_func(filename):

    start_time = time()

    def process_func(block_count, block_size, total_size):
        downloaded_size = block_count * block_size

        percent = int(downloaded_size * 100 / total_size)
        if percent >= 100:
            percent = 100
        elif percent <= 0:
            percent = 0
        percent_text = str(percent) + '%'

        bar = (percent * 20) / 100
        bar_text = '[%-20s]' % ('=' * bar)

        speed = downloaded_size / (time() - start_time) / 1024.0
        speed_text = '%.2fK/s' % speed

        filesize = total_size / 1024.0 ** 2
        filesize_text = '%.2fM' % filesize

        line = ' '.join((filename, filesize_text, bar_text,
                         speed_text, percent_text))
        sys.stdout.write('\r')
        sys.stdout.write(line)
        if percent == 100:
            sys.stdout.write('\n')
        sys.stdout.flush()

    return process_func

def retrieve_file(remote_url, local_url, process_filename):
    urlretrieve(remote_url, local_url, create_process_func(process_filename))
