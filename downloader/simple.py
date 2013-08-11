#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
from time import time
import urllib2
from id3 import fill_tags

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

def download_song(song, save_folder='./', best_quality=True):
    filename = '%s - %s.mp3' % (song.artist, song.title)
    filepath = os.path.join(save_folder, filename)
    if os.path.exists(filepath):
        return

    if best_quality:
        remote_url = song.best_quality_mp3_url
    else:
        remote_url = song.default_mp3_url
    local_url = filepath + '.part'

    urlretrieve(remote_url, local_url, create_process_func(filepath))
    fill_tags(local_url, song)
    os.rename(local_url, filepath)

def download_songs(songs, save_folder='./', best_quality=True):
    for song in songs:
        download_song(song, save_folder, best_quality)

def download_album(album, save_folder='./', best_quality=True):
    parent_folder = os.path.join(save_folder, u'[专辑]' + album.title)
    if not os.path.exists(parent_folder):
        os.mkdir(parent_folder)
    download_songs(album.songs, parent_folder, best_quality)

def download_albums(albums, save_folder='./', best_quality=True):
    for album in albums:
        download_album(album, save_folder, best_quality)

def download_playlist(playlist, save_folder='./', best_quality=True):
    parent_folder = os.path.join(save_folder, u'[歌单]' + playlist.title)
    if not os.path.exists(parent_folder):
        os.mkdir(parent_folder)
    download_songs(playlist.songs, parent_folder, best_quality)

def download_playlists(playlists, save_folder='./', best_quality=True):
    for playlist in playlists:
        download_playlist(playlist, save_folder, best_quality)
