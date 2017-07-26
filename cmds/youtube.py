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
        except Exception as e:
			embed=discord.Embed(title="Error", description="Error when trying to retrieve data from https://www.youtube.com/results", color=0xff0000)
			embed.set_thumbnail(url='http://i.imgur.com/dx87cAe.png')
			embed.add_field(name="Reason", value=e.args[1], inline=False)
			await dclient.send_message(channel, embed=embed)
            return True, 'HTTP', 'Error when trying to retrieve data from https://www.youtube.com/results. ERROR: {}'.format(e.args[1])
    else:
        await dclient.send_message(channel, '{}, **USAGE:** {}youtube <to-search>'.format(mention, cmd_char))
    return False
