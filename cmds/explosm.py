from bs4 import BeautifulSoup
import requests


# Explosm command
async def ex(dclient, channel, mention):
    try:
        b = BeautifulSoup(requests.get('http://explosm.net/rcg', 'html.parser'))
        v = b.find('div', id='rcg-comic')
        if not v:
            await dclient.send_message(channel, 'Unable to find the comic, {}!'.format(mention))
        else:
            await dclient.send_message(channel, '{}'.format(v.find('img')))
    except Exception as exc:
        await dclient.send_message(channel, 'Unable to complete this task, {}! Please let the admins know!'
                                   .format(mention))
        print(exc)
