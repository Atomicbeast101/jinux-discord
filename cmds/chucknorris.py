import aiohttp


# Chuck Norris command
async def ex(dclient, channel):
    async with aiohttp.ClientSession() as s:
        async with s.get('https://api.chucknorris.io/jokes/random') as r:
            d = await r.json()
            await dclient.send_message(channel, '{}'.format(d['value']))
