from bs4 import BeautifulSoup
import requests


# Youtube command
async def ex(c, ch, m, a, CMD_CHAR):
    if len(a) > 0:
        a.replace(" ", "+")
        try:
            b = BeautifulSoup(requests.get('https://www.youtube.com/results?search_query={}'.format(a)).text,
                              'html.parser')
            v = b.find('div', id='results').find_all('div', class_='yt-lockup-content')
            if not v:
                await c.send_message(ch, 'Unable to find any results, {}!'.format(m))
            else:
                i, f = 0, False
                while not f and i < 20:
                    h = v[i].find('a', class_='yt-uix-sessionlink')['href']
                    if h.startswith('/watch'):
                        f = True
                    i += 1
                if not f:
                    await c.send_message(ch, 'Unable to find the link in the results, {}!'.format(m))
                else:
                    await c.send_message(ch, 'https://youtube.com{}'.format(h))
        except Exception as exc:
            await c.send_message(ch, 'Unable to complete this task, {}! Please let the admins know!'.format(m))
            print(exc)
    else:
        await c.send_message(ch, '{}, **USAGE:** {}youtube <to-search>'.format(m, CMD_CHAR))
