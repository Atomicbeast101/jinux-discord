import aiohttp


# 8ball command
async def ex(c, ch, a, m, CMD_CHAR):
    if len(a.split(' ')) > 0:
        a.replace(' ', '+')
        async with aiohttp.ClientSession() as s:
            async with s.get('http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag={}'.format(a)) as r:
                d = await r.json()
                await c.send_message(ch, '{}'.format(d['data']['fixed_height_downsampled_url']))
    else:
        await c.send_message(ch, '{}, **USAGE:** {}8ball <Question...>'.format(m, CMD_CHAR))
