import aiohttp
import re

def is_int(a):
    try:
        int(a)
        return True
    except ValueError:
        return False


# Reddit command
async def ex(dclient, private_channel, public_channel, mention, a):
    a = a.split(' ')
    url = 'https://reddit.com/.json'
    max_subs = 5
    title = "Reddit's Front Page"
    subreddit = False
    valid = True
    if len(a) > 0 and a[0] is not '':
        if is_int(a[0]):
            max_subs = int(a[0])
            if max_subs < 1 or max_subs > 10:
                await dclient.send_message(public_channel, '{}, you can request only up to 10 submissions!'.format(mention))
                valid = False
        else:
            subreddit_link = a[0].lower()
            url = 'https://reddit.com/r/{}.json'.format(subreddit_link)
            if len(a) > 1:
                if is_int(a[1]):
                    max_subs = int(a[1])
                    if max_subs < 1 or max_subs > 10:
                        await dclient.send_message(public_channel, '{}, you can request only up to 10 submissions!'.format(mention))
                        valid = False
            title = '/r/{}'.format(subreddit_link)
            subreddit = True
    if valid:
        async with aiohttp.ClientSession() as s:
            async with s.get(url) as r:
                d = await r.json()
                r = '''**{} Hot Submissions in {}:**
'''.format(str(max_subs), title)
                cnt = 1
                if subreddit:
                    for sr in d['data']['children']:
                        if not sr['data']['author'] == 'AutoModerator':
                            title = str(sr['data']['title'].encode('utf-8'))[2:-1]
                            url = sr['data']['permalink']
                            r += '''**{})** {}
    <https://reddit.com{}>

'''.format(cnt, title, url)
                            cnt += 1
                            if cnt > max_subs:
                                break
                else:
                    for sr in d['data']['children']:
                        title = str(sr['data']['title'].encode('utf-8'))[2:-1]
                        url = sr['data']['permalink']
                        r += '''**{})** {}
    <https://reddit.com{}>

'''.format(cnt, title, url)
                        cnt += 1
                        if cnt > max_subs:
                            break
        await dclient.send_message(private_channel, r)
        await dclient.send_message(public_channel, '{}, I sent the list in a private message.'.format(mention))
