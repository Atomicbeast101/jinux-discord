import aiohttp


# 8ball command
async def ex(dclient, channel, a, mention, cmd_char):
    if len(a.split(' ')) > 0:
        a.replace(' ', '+')
        async with aiohttp.ClientSession() as s:
            async with s.get('http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag={}'.format(a)) as r:
                d = await r.json()
                await dclient.send_message(channel, '{}'.format(d['data']['fixed_height_downsampled_url']))
    else:
        await dclient.send_message(channel, '{}, **USAGE:** {}8ball <Question...>'.format(mention, cmd_char))
