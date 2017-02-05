import paw


# Reddit command
async def ex(c, pch, dch, m, a, CMD_CHAR):
    a = a.split(' ')
    if len(a) > 0:
        a = a[0].lower()
        try:
            re = paw.Reddit()
            r = '''20 Hot Submissions from Subreddit: `{}`'''.format(a)
            for p in re.subreddit(a).hot(limit=20):
                r += '''<{}>'''.format(p.shortlink)
            await c.send_message(pch, '{}'.format(r))
            await c.send_message(dch, '{}, I sent you a list of links to different submissions in `{}` subreddit in a '
                                      'private message!'.format(m, a))
        except Exception as exc:
            await c.send_message(dch, '{}, unable to find the submissions from the subreddit `{}`!'.format(m, a))
            print(exc)

    else:
        await c.send_message(dch, '{}, **USAGE:** {}reddit <subreddit>'.format(m, CMD_CHAR))
