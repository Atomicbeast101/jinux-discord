import aiohttp


# Be Like Bill command
async def ex(dclient, channel):
    async with aiohttp.ClientSession() as s:
        async with s.get('http://belikebill.azurewebsites.net/billgen-API.php?default=1') as r:
            d = await r.json()
            await dclient.send_message(channel, '{}'.format(d['value']))
