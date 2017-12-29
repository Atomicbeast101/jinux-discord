from aiohttp import ClientSession
from bs4 import BeautifulSoup
from random import choice
from requests import get


# Check if value is an int
def is_int_value(_value):
    try:
        int(_value)
        return True
    except ValueError:
        return False


def usage_msg(_cmd, _mention, _cmdchar):
    return ':warning: {} **USAGE:** {}{}'.format(_mention, _cmdchar, _cmd)


class XKCD:
    def __init__(self):
        self.url_latest = 'https://xkcd.com/info.0.json'
        self.url_get_id = 'https://xkcd.com/{}/info.0.json'
        self.url_random_feed = 'https://xkcd.com/archive/'

    async def execute(self, _dclient, _channel, _mention, _cmdchar, _msg):
        _msg = _msg.split(' ')
        if len(_msg) > 0:
            if _msg[0].lower() == 'latest':
                async with ClientSession() as cs:
                    async with cs.get(self.url_latest) as response:
                        data = await response.json()
                        await _dclient.send_message(_channel, '''**Title:** {}
**Comic ID:** {}
{}'''.format(data['safe_title'], data['num'], data['img']))
            elif is_int_value(_msg[0]):
                comic_id = int(_msg[0])
                try:
                    async with ClientSession() as cs:
                        async with cs.get(self.url_get_id.format(comic_id)) as response:
                            data = await response.json()
                            await _dclient.send_message(_channel, '''**Title:** {}
**Comic ID:** {}
{}'''.format(data['safe_title'], data['num'], data['img']))
                except Exception:
                    await _dclient.send_message(_channel, ':warning: {} Unable to retrieve comic for ID `{}`! Perhaps '
                                                          'it\'s the wrong one?'.format(_mention, comic_id))
            else:
                await _dclient.send_message(_channel, usage_msg('xkcd <latest|# comic id>', _mention,
                                                                _cmdchar))
        else:
            bs = BeautifulSoup(get(self.url_random_feed).text, 'html.paser')
            id_list = bs.find('div', id='middleContainer').find_all('a')
            comic_id = choice(id_list)['href']
            comic_id = comic_id.replace('/', '')
            async with ClientSession() as cs:
                async with cs.get(self.url_get_id.format(comic_id)) as response:
                    data = await response.json()
                    await _dclient.send_message(_channel, '''**Title:** {}
**Comic ID:** {}
{}'''.format(data['safe_title'], data['num'], data['img']))
