from bin import yt_title


def create_yt_url(_youtube_id):
    return 'https://www.youtube.com/watch?v={}'.format(_youtube_id)


class Song:
    def __init__(self):
        self.youtube_id = ''
        self.name = ''

    def set(self, _youtube_id):
        valid, title = yt_title.get_yt_title(_youtube_id)

        if valid:
            self.youtube_id = _youtube_id
            self.name = title
            return True
        else:
            return False

    def full_set(self, _youtube_id, _name):
        self.youtube_id = _youtube_id
        self.name = _name

    def get_youtube_url(self):
        return create_yt_url(self.youtube_id)
