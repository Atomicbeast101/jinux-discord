import aiohttp


# manages -chucknorris
class ChuckNorris:
    async def get_joke(self, log, dclient, msg):
        async with aiohttp.ClientSession() as s:
            async with s.get('https://api.chucknorris.io/jokes/random') as r:
                data = await r.json()
                await dclient.send_message(msg.channel, data['value'])
