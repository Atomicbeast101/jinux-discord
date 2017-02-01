import aiohttp


# Chuck Norris command
async def ex(c, ch):
    async with aiohttp.ClientSession() as s:
        async with s.get('https://api.chucknorris.io/jokes/random') as r:
            d = await r.json()
            await c.send_message(ch, '{}'.format(d['value']))
