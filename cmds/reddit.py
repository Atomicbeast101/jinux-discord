import aiohttp


# Reddit command
async def ex(c, pch, dch, m, a, CMD_CHAR):
    a = a.split(' ')
    if len(a) > 0:
        a = a[0].lower()
        async with aiohttp.ClientSession() as s:
            async with s.get('https://www.reddit.com/r/{}/.json'.format(a)) as r:
                d = await r.json()
                if d['message'] is not 'Forbidden':
                    r = '''20 Hot Submissions from Subreddit: `{}`'''.format(a)
                    co = 0
                    for i in d['data']['children']:
                        if i['selftext_html'] is None:
                            co += 1
                            r += '''<{}>'''.format('https://www.reddit.com' + i['selftext_html'])
                        if co >= 20:
                            break
                    await c.send_message(pch, '{}'.format(r))
                    await c.send_message(dch, '{}, I sent it in a private message.'.format(m))
                else:
                    await c.send_message(dch, '{}, unable to get submissions from subreddit `{}` because it doesnt '
                                              'exist!'.format(m, a))
    else:
        await c.send_message(dch, '{}, **USAGE:** {}reddit <subreddit>'.format(m, CMD_CHAR))
