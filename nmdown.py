#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
from argparse import ArgumentParser
from cloudmusic import make_songs, make_albums, make_playlists, make_artists
from downloader.download import (
        download_songs, download_albums, download_playlists, download_artists)

def print_songs(songs, indent=0):
    for song in songs:
        if indent:
            print ' ' * indent,
        print song.id, song.title, song.best_quality_mp3_url
    print

def print_albums(albums):
    for album in albums:
        print album.id, album.title
        print_songs(album.songs, 2)

def print_playlists(playlists):
    for playlist in playlists:
        print playlist.id, playlist.title
        print_songs(playlist.songs, 2)

def test():
    songs = make_songs(['442723', '442727'])
    print_songs(songs)

    albums = make_albums(['42967'])
    print_albums(albums)

    playlists = make_playlists(['190990'])
    print_playlists(playlists)

def down(url, config):
    reg = re.compile('http://music.163.com/#/(.+?)\?id=(.+)')
    matches = reg.findall(url)
    if not matches:
        return

    output_folder = config['output']
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    type, id = matches[0]
    if type == 'song':
        songs = make_songs([id])
        download_songs(songs, config)
    elif type == 'album':
        albums = make_albums([id])
        download_albums(albums, config)
    elif type == 'playlist':
        playlists = make_playlists([id])
        download_playlists(playlists, config)
    elif type == 'artist':
        artists = make_artists([id])
        download_artists(artists, config)

def read_urls_from_file(filename):
    with open(filename) as file:
        text = file.read()
    lines = map(lambda l: l.strip(), text.split('\n'))
    urls = filter(lambda l: l.startswith('http://'), lines)
    return urls

def argparser():
    parser = ArgumentParser(description='网易云音乐批量下载工具')
    addarg = parser.add_argument
    addarg('uri', metavar='uri', nargs='+', type=str,
           help='歌曲/专辑/歌单/艺术家地址，包含地址的文件名')
    addarg('-q', '--quality', default='normal',
           choices=['normal', 'low', 'medium', 'high', 'best'],
           help='优先下载音质，默认是 normal')
    addarg('-l', '--lyric', action='store_true',
           help='同时下载歌词（如果有）')
    addarg('-c', '--cover', action='store_true',
           help='替换为高分辨率封面')
    addarg('-o', '--output', type=str, default='./',
           help='保存目录')
    return parser

def main():
    args = argparser().parse_args().__dict__
    uris = args.pop('uri')

    urls = []
    for uri in uris:
        if uri.startswith('http://'):
            urls.append(uri)
        else:
            urls.extend(read_urls_from_file(uri))

    config = args
    for url in urls:
        down(url, config)

if __name__ == '__main__':
    main()
