#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys
from cloudmusic import make_songs, make_albums, make_playlists
from downloader.simple import (
        download_songs, download_albums, download_playlists)

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

def down(url):
    reg = re.compile('http://music.163.com/#/m/(.+?)\?id=(.+)')
    matches = reg.findall(url)
    if not matches:
        return

    type, id = matches[0]
    if type == 'song':
        songs = make_songs([id])
        download_songs(songs)
    elif type == 'album':
        albums = make_albums([id])
        download_albums(albums)
    elif type == 'playlist':
        playlists = make_playlists([id])
        download_playlists(playlists)

def main():
    for url in sys.argv[1:]:
        down(url)

if __name__ == '__main__':
    main()
