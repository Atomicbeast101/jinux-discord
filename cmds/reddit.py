import aiohttp


# Reddit command
async def ex(c, pch, dch, m, a):
    a = a.split(' ')
    if len(a) == 0:
        async with aiohttp.ClientSession() as s:
            async with s.get('https://reddit.com/.json') as r:
                d = await r.json()
                r = '''Hot 10 Submissions in Reddit's Front Page:
'''
                cnt = 1
                for s in d['data']['children']:
                    r += '''{}) {}
    {}
'''.format(cnt, s['data']['secure_media']['oembed']['title'])
                    cnt += 1
                await c.send_message(pch, r)
                await c.send_message(dch, '{}, I sent the list in a private message.'.format(m))
    else:
        a = a[0]
        async with aiohttp.ClientSession() as s:
            async with s.get('https://reddit.com/r/{}/.json'.format(a)) as r:
                d = await r.json()
                r = '''10 Hot Submissions in /r/{}:
'''.format(a)
                cnt = 1
                for sr in d['data']['children']:
                    if sr['data']['domain'] != 'self.movies':
                        r += '''{}) {}
    {}
'''.format(cnt, sr['data']['secure_media']['oembed']['title'])
                    cnt += 1
                await c.send_message(pch, r)
                await c.send_message(dch, '{}, I sent the list in a private message.'.format(m))
