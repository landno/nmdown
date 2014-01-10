import json
from .utils import read_url
from .song import make_song_with_detail

DETAIL_TPL = 'http://music.163.com/api/playlist/detail?id=%(id)s'


class Playlist(object):

    def __init__(self, id):
        self.id = id
        self.load_detail()
        self.load_songs()

    def load_detail(self):
        text = read_url(self.detail_url)
        self.detail = json.loads(text)['result']

    def load_songs(self):
        self.songs = make_song_with_detail(self.detail['tracks'])

    @property
    def detail_url(self):
        return DETAIL_TPL % dict(id=self.id)

    @property
    def title(self):
        return self.detail['name']

    @property
    def track_number(self):
        return self.detail['trackCount']

    @property
    def tags(self):
        return self.detail['tags']


def make_playlists(ids):
    return [Playlist(id) for id in ids]
