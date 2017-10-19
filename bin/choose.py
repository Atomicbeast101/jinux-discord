import discord
import random


# manages -choose
class Choose:
    async def decide(self, log, dclient, msg, cmd_char):
        options = msg.content[8:].split(' ')
        if len(options) >= 2:
            await dclient.send_message(msg.channel, '<@{}>, I choose `{}`!'.format(msg.author.id,
                                                                                   random.choice(options)))
        else:
            embed = discord.Embed(title='Invalid Input',
                                  description='{}choose <options>. Must have two or more options. (Ex: {}choose red '
                                              'green)'.format(msg.author.id, cmd_char),
                                  color=0xff0000)
            embed.set_thumbnail(url='http://i.imgur.com/dx87cAe.png')
            await dclient.send_message(msg.channel, embed=embed)
