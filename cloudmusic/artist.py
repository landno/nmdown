#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from .utils import read_url
from .album import make_albums

DETAIL_TPL = 'http://music.163.com/api/artist/albums/%(id)s?id=%(id)s&offset=0&total=true&limit=1024'


class Artist(object):

    def __init__(self, id):
        self.id = id
        self.load_detail()
        self.load_albums()

    def load_detail(self):
        text = read_url(self.detail_url)
        self.detail = json.loads(text)

    def load_albums(self):
        ids = [d['id'] for d in self.detail['hotAlbums']]
        self.albums = make_albums(ids)

    @property
    def detail_url(self):
        return DETAIL_TPL % dict(id=self.id)

    @property
    def name(self):
        return self.detail['artist']['name']


def make_artists(ids):
    return [Artist(id) for id in ids]
