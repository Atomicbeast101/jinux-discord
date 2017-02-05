from paw import Reddit


# Reddit command
async def ex(c, ch, m, a, CMD_CHAR):
    a = a.split(' ')
    if len(a) > 0:
        try:
            re = Reddit()
            r = '''20 Hot Topics from Subreddit: `{}`'''.format(a[0].lower())
            for p in re.subreddit(a[0].lower()).hot(limit=20):
                r += '''<{}>'''.format(p.shortlink)

        except Exception as exc:
            await c.send_message(ch, '{}, error when trying to retrieve top 10 posts from a sub-reddit!'.format(m))
            print(exc)

    else:
        await c.send_message(ch, '{}, **USAGE:** {}reddit <sub-reddit>'.format(m, CMD_CHAR))
