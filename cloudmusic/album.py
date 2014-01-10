#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from .utils import timestamp2datetime, read_url
from .song import make_song_with_detail

DETAIL_TPL = 'http://music.163.com/api/album/%(id)s'


class Album(object):

    def __init__(self, id):
        self.id = id
        self.load_detail()
        self.load_songs()

    def load_detail(self):
        text = read_url(self.detail_url)
        self.detail = json.loads(text)['album']

    def load_songs(self):
        self.songs = make_song_with_detail(self.detail['songs'])

    @property
    def detail_url(self):
        return DETAIL_TPL % dict(id=self.id)

    @property
    def title(self):
        return self.detail['name']

    @property
    def track_number(self):
        return self.detail['size']

    @property
    def publisher(self):
        return self.detail['company']

    @property
    def publish_year(self):
        return self.album_publish_datetime.strftime('%Y')

    @property
    def publish_datetime(self):
        return timestamp2datetime(self.detail['publishTime'])


def make_albums(ids):
    return [Album(id) for id in ids]
