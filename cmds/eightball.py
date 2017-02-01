import aiohttp


# 8ball command
async def ex(c, ch, m, q, CMD_CHAR):
    if len(q.split(' ')) >= 1:
        q.replace(' ', '%')
        q.replace('?', '%3F')
        q.replace(',', '%2C')
        async with aiohttp.ClientSession() as s:
            async with s.get('https://8ball.delegator.com/magic/JSON/{}'.format(q)) as r:
                d = await r.json()
                await c.send_message(ch, '{}, {}'.format(m, d['magic']['answer']))
    else:
        await c.send_message(ch, '{}, **USAGE:** {}8ball <Question...>'.format(m, CMD_CHAR))
