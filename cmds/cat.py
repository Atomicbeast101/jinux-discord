import aiohttp


# Cat command
async def ex(c, ch):
    async with aiohttp.ClientSession() as s:
        async with s.get('http://random.cat/meow') as r:
            d = await r.json()
            await c.send_message(ch, '{}'.format(d['file']))
