from bs4 import BeautifulSoup
from random import choice
import requests
import aiohttp


# xkcd command
async def ex(dclient, channel, a):
    if len(a) > 0:
        a = a.split(' ')[0]
        if a == 'latest':
            async with aiohttp.ClientSession() as s:
                async with s.get('https://xkcd.com/info.0.json') as r:
                    d = await r.json()
                    await dclient.send_message(channel, '''Title: {}
{}'''.format(d['safe_title'], d['img']))
        else:
            b = BeautifulSoup(requests.get('https://xkcd.com/archive/').text, 'html.parser')
            ids = b.find('div', id='middleContainer').find_all('a')
            idr = choice(ids)['href']
            idr.replace('/', '')
            async with aiohttp.ClientSession() as s:
                async with s.get('https://xkcd.com/{}/info.0.json'.format(idr)) as r:
                    d = await r.json()
                    await dclient.send_message(channel, '''Title: {}
{}'''.format(d['safe_title'], d['img']))
    else:
        b = BeautifulSoup(requests.get('https://xkcd.com/archive/').text, 'html.parser')
        ids = b.find('div', id='middleContainer').find_all('a')
        idr = choice(ids)['href']
        idr.replace('/', '')
        async with aiohttp.ClientSession() as s:
            async with s.get('https://xkcd.com/{}/info.0.json'.format(idr)) as r:
                d = await r.json()
                await dclient.send_message(channel, '''Title: {}
{}'''.format(d['safe_title'], d['img']))
