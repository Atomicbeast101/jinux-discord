import aiohttp


# Reddit command
async def ex(dclient, private_channel, public_channel, mention, a):
    a = a.split(' ')
    if len(a) == 1:
        async with aiohttp.ClientSession() as s:
            async with s.get('https://reddit.com/.json') as r:
                d = await r.json()
                r = '''Hot 10 Submissions in Reddit's Front Page:
'''
                cnt = 1
                for sr in d['data']['children']:
                    title = sr['data']['title']
                    url = sr['data']['permalink']
                    r += '''{}) {}
    <https://reddit.com{}>
'''.format(cnt, title, url)
                    cnt += 1
                await dclient.send_message(private_channel, r)
                await dclient.send_message(public_channel, '{}, I sent the list in a private message.'.format(mention))
    else:
        a = a[1]
        async with aiohttp.ClientSession() as s:
            async with s.get('https://reddit.com/r/{}/.json'.format(a)) as r:
                d = await r.json()
                r = '''10 Hot Submissions in /r/{}:
'''.format(a)
                cnt = 1
                for sr in d['data']['children']:
                    if not sr['data']['author'] != 'AutoModerator':
                        title = sr['data']['title']
                        url = sr['data']['permalink']
                        r += '''{}) {}
    <https://reddit.com{}>
'''.format(cnt, title, url)
                    cnt += 1
                await dclient.send_message(private_channel, r)
                await dclient.send_message(public_channel, '{}, I sent the list in a private message.'.format(mention))
