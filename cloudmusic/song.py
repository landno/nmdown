#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
from .utils import timestamp2datetime, read_url
from .hasher import make_hash

MAIN_TPL = 'http://music.163.com/#/m/song?id=%(id)s'
DETAIL_TPL = 'http://music.163.com/api/song/detail/?ids=[%(ids)s]'
MEDIA_TPL = 'http://music.163.com/api/song/media?id=%(id)s'
MP3_TPL = 'http://m1.music.126.net/%(hash)s/%(dfsId)s.mp3'

album_cover_cache = {}


class Song(object):

    def __init__(self, id=None):
        self.id = id

        if self.id is not None:
            self.load_detail()

    def init_with_detail(self, detail):
        self.id = detail['id']
        self.detail = detail

    def load_detail(self):
        text = read_url(self.detail_url)
        self.detail = json.loads(text)['songs'][0]

    @property
    def media(self):
        # 需要发送多一次 http 请求，因此使用 lazy 载入
        if not hasattr(self, '_media'):
            text = read_url(self.media_url)
            self._media = json.loads(text)
        return self._media

    @property
    def main_url(self):
        return MAIN_TPL % dict(id=self.id)

    @property
    def detail_url(self):
        return DETAIL_TPL % dict(ids=self.id)

    @property
    def media_url(self):
        return MEDIA_TPL % dict(id=self.id)

    @property
    def default_mp3_url(self):
        return self.detail['mp3Url']

    def _x_quality_mp3_url(self, dfsId):
        return MP3_TPL % dict(hash=make_hash(dfsId), dfsId=dfsId)

    @property
    def low_quality_mp3_url(self):
        dfsId = self.detail['lMusic']['dfsId']
        return self._x_quality_mp3_url(dfsId)

    @property
    def medium_quality_mp3_url(self):
        info = self.detail['mMusic']
        if info is None:
            return None
        dfsId = info['dfsId']
        return self._x_quality_mp3_url(dfsId)

    @property
    def high_quality_mp3_url(self):
        info = self.detail['hMusic']
        if info is None:
            return None
        dfsId = info['dfsId']
        return self._x_quality_mp3_url(dfsId)

    @property
    def best_quality_mp3_url(self):
        dfsId = self.detail['bMusic']['dfsId']
        return self._x_quality_mp3_url(dfsId)

    def _x_quality_mp3_bitrate(self, bitrate):
        return bitrate / 1000

    @property
    def low_quality_mp3_bitrate(self):
        bitrate = self.detail['lMusic']['bitrate']
        return self._x_quality_mp3_bitrate(bitrate)

    @property
    def medium_quality_mp3_bitrate(self):
        info = self.detail['mMusic']
        if info is None:
            return None
        bitrate = info['bitrate']
        return self._x_quality_mp3_bitrate(bitrate)

    @property
    def high_quality_mp3_bitrate(self):
        info = self.detail['hMusic']
        if info is None:
            return None
        bitrate = info['bitrate']
        return self._x_quality_mp3_bitrate(bitrate)

    @property
    def best_quality_mp3_bitrate(self):
        bitrate = self.detail['bMusic']['bitrate']
        return self._x_quality_mp3_bitrate(bitrate)

    @property
    def title(self):
        return self.detail['name']

    @property
    def title_for_filename(self):
        return self.title.replace('/', ' ')

    @property
    def artist(self):
        return ' & '.join(self.artists)

    @property
    def artists(self):
        return map(lambda a: a['name'], self.detail['artists'])

    @property
    def album_id(self):
        return self.detail['album']['id']

    @property
    def album_title(self):
        return self.detail['album']['name']

    @property
    def album_track_index(self):
        return self.detail['position']

    @property
    def album_track_number(self):
        return self.detail['album']['size']

    @property
    def album_publisher(self):
        return self.detail['album']['company']

    @property
    def album_publish_year(self):
        return self.album_publish_datetime.strftime('%Y')

    @property
    def album_publish_datetime(self):
        return timestamp2datetime(self.detail['album']['publishTime'])

    @property
    def album_cover_url(self):
        return self.detail['album']['picUrl']

    @property
    def album_cover_data(self):
        url = self.album_cover_url
        if url not in album_cover_cache:
            data = read_url(url)
            album_cover_cache[url] = data
        return album_cover_cache[url]

    @property
    def album_cover_mimetype(self):
        png_magic = '\x89PNG\x0d'
        if self.album_cover_data.startswith(png_magic):
            return 'image/png'
        else:
            return 'image/jpeg'

    @property
    def lyric(self):
        if 'lyric' in self.media:
            return self.media['lyric']
        else:
            return None


def make_song_with_detail(details):
    songs = []
    for d in details:
        song = Song()
        song.init_with_detail(d)
        songs.append(song)
    return songs


def make_songs(ids):
    url = DETAIL_TPL % dict(ids=','.join(ids))
    text = read_url(url)
    details = json.loads(text)['songs']
    return make_song_with_detail(details)
