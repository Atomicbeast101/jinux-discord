from traceback import format_exc
import aiohttp
import discord


# manages -cat
class Cat:
    def __init__(self):
        self.embed = discord.Embed(title='Error',
                                   description='Error when trying to retrieve data from \'http://random.cat/meow\'!',
                                   color=0xff0000)
        self.embed.set_thumbnail(url='http://i.imgur.com/dx87cAe.png')

    async def get_pic(self, log, dclient, channel):
        msg = None
        try:
            async with aiohttp.ClientSession as s:
                async with s.get('http://random.cat/meow') as r:
                    data = await r.json()
                    msg = await dclient.send_message(channel, data['file'])
        except Exception:
            msg = await dclient.send_message(channel, embed=self.embed)
            log.error('Error when trying to retrieve data from \'http://random.cat/meow\'!\n{}'.format(format_exc()))
        return msg
