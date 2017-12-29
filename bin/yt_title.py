from bs4 import BeautifulSoup
from requests import get


def get_yt_title(_youtube_id):
    try:
        bs = BeautifulSoup(get('https://www.youtube.com/watch?v={}'.format(_youtube_id)).text, 'html.parser')
        return True, bs.findAll('span', {'class': 'watch-title'})[0].get_text().strip()
    except Exception:
        return False, None
