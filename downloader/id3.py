import logging
logger = logging.getLogger('eyed3.id3.frames')
logger.setLevel(logging.ERROR)

from eyed3.mp3 import Mp3AudioFile
from eyed3.id3 import frames
frames.Frame.__lt__ = lambda self, other: self.__class__.__name__ < other.__class__.__name__


def fill_tags(filename, song, config):
    mp3file = Mp3AudioFile(filename)
    mp3file.initTag()
    tag = mp3file.tag

    tag.title = song.title
    tag.artist = song.artist
    tag.album = song.album_title
    tag.track_num = song.album_track_index, song.album_track_number
    tag.publisher = song.album_publisher
    tag.recording_date = song.album_publish_datetime.year
    tag.audio_file_url = song.main_url

    if config['cover']:
        tag.images.set(0, song.album_cover_data, song.album_cover_mimetype, '')

    tag.save()
