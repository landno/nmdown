#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from id3 import fill_tags
from retrieve import retrieve_file

def download_lyric(song, config):
    filename = '%s - %s.lrc' % (song.artist, song.title_for_filename)
    filepath = os.path.join(config['output'], filename)
    if os.path.exists(filepath):
        return

    with open(filepath, 'w') as file:
        file.write(song.lyric.encode('UTF-8'))

def download_audio(song, config):
    filename = '%s - %s.mp3' % (song.artist, song.title_for_filename)
    filepath = os.path.join(config['output'], filename)
    if os.path.exists(filepath):
        return

    quality = config['quality']
    if quality == 'default':
        remote_url = song.default_mp3_url
    else:
        remote_url = getattr(song, quality + '_quality_mp3_url')
    local_url = filepath + '.part'

    retrieve_file(remote_url, local_url, filepath)
    fill_tags(local_url, song)
    os.rename(local_url, filepath)

def download_song(song, config):
    download_audio(song, config)
    if config['lyric'] and song.lyric:
        download_lyric(song, config)

def download_songs(songs, config):
    for song in songs:
        download_song(song, config)

def download_album(album, config):
    song_folder = u'[专辑]' + album.title
    album_folder = os.path.join(config['output'], song_folder)
    if not os.path.exists(album_folder):
        os.mkdir(album_folder)

    config = config.copy()
    config['output'] = album_folder
    download_songs(album.songs, config)

def download_albums(albums, config):
    for album in albums:
        download_album(album, config)

def download_playlist(playlist, config):
    song_folder =  u'[歌单]' + playlist.title
    playlist_folder = os.path.join(config['output'], song_folder)
    if not os.path.exists(playlist_folder):
        os.mkdir(playlist_folder)

    config = config.copy()
    config['output'] = playlist_folder
    download_songs(playlist.songs, config)

def download_playlists(playlists, config):
    for playlist in playlists:
        download_playlist(playlist, config)

def download_artist(artist, config):
    album_folder = u'[艺术家]' + artist.name
    artist_folder = os.path.join(config['output'], album_folder)
    if not os.path.exists(artist_folder):
        os.mkdir(artist_folder)

    config = config.copy()
    config['output'] = artist_folder
    download_albums(artist.albums, config)

def download_artists(artists, config):
    for artist in artists:
        download_artist(artist, config)
