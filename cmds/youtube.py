from bs4 import BeautifulSoup
import requests


# Youtube command
async def ex(dclient, channel, mention, a, cmd_char):
    if len(a) > 0:
        a.replace(" ", "+")
        try:
            b = BeautifulSoup(requests.get('https://www.youtube.com/results?search_query={}'.format(a)).text,
                              'html.parser')
            v = b.find('div', id='results').find_all('div', class_='yt-lockup-content')
            if not v:
                await dclient.send_message(channel, 'Unable to find any results, {}!'.format(mention))
            else:
                i, f = 0, False
                while not f and i < 20:
                    h = v[i].find('a', class_='yt-uix-sessionlink')['href']
                    if h.startswith('/watch'):
                        f = True
                    i += 1
                if not f:
                    await dclient.send_message(channel, 'Unable to find the link in the results, {}!'.format(mention))
                else:
                    await dclient.send_message(channel, 'https://youtube.com{}'.format(h))
        except Exception as exc:
            await dclient.send_message(channel, 'Unable to complete this task, {}! Please let the admins know!'
                                       .format(mention))
            print(exc)
    else:
        await dclient.send_message(channel, '{}, **USAGE:** {}youtube <to-search>'.format(mention, cmd_char))
