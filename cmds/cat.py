import aiohttp


# Cat command
async def ex(dclient, channel):
    async with aiohttp.ClientSession() as s:
        async with s.get('http://random.cat/meow') as r:
            d = await r.json()
            await dclient.send_message(channel, '{}'.format(d['file']))
