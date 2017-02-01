from config import CMD_CHAR
from bs4 import BeautifulSoup
from random import choose
import requests
import aiohttp


# xkcd command
async def ex(c, ch, m, a):
    if len(a) > 0:
        a = a.split(' ')[0]
        if a == 'latest':
            async with aiohttp.ClientSession() as s:
                async with s.get('https://xkcd.com/info.0.json') as r:
                    d = await r.json()
                    await c.send_message(ch, '''Title: {}
                                                {}'''.format(d['safe_title'], d['img']))
        else:
            b = BeautifulSoup(requests.get('https://xkcd.com/archive/').text, 'html.parser')
            ids = b.find('div', id='middleContainer').find_all('a')
            idr = choose(ids)['href']
            idr.replace('/', '')
            async with aiohttp.ClientSession() as s:
                async with s.get('https://xkcd.com/{}/info.0.json'.format(idr)) as r:
                    d = await r.json()
                    await c.send_message(ch, '''Title: {}
                                                {}'''.format(d['safe_title'], d['img']))
    else:
        b = BeautifulSoup(requests.get('https://xkcd.com/archive/').text, 'html.parser')
        ids = b.find('div', id='middleContainer').find_all('a')
        idr = choose(ids)['href']
        idr.replace('/', '')
        async with aiohttp.ClientSession() as s:
            async with s.get('https://xkcd.com/{}/info.0.json'.format(idr)) as r:
                d = await r.json()
                await c.send_message(ch, '''Title: {}
                                                        {}'''.format(d['safe_title'], d['img']))
