#!/usr/bin/env python
# -*- coding: utf-8 -*-

import eyed3.mp3

def fill_tags(filename, song, config):
    tag = eyed3.mp3.Mp3AudioFile(filename).tag

    tag.title = song.title
    tag.artist = song.artist
    tag.album = song.album_title
    tag.track_num = song.album_track_index, song.album_track_number
    tag.publisher = song.album_publisher
    tag.recording_date = song.album_publish_datetime
    tag.audio_file_url = song.main_url

    if config['cover']:
        image = tag.images.get(u'')
        image.image_data = song.album_cover_data
        image.mime_type = song.album_cover_mimetype

    tag.save()
