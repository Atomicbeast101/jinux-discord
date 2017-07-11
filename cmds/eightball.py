import aiohttp


# 8ball command
async def ex(dclient, channel, mention, question, cmd_char):
    if len(question.split(' ')) >= 1:
        question.replace(' ', '%')
        question.replace('?', '%3F')
        question.replace(',', '%2C')
		try:
			async with aiohttp.ClientSession() as s:
				async with s.get('https://8ball.delegator.com/magic/JSON/{}'.format(question)) as r:
					d = await r.json()
					await dclient.send_message(channel, '{}, {}'.format(mention, d['magic']['answer']))
		except Exception ex:
			embed=discord.Embed(title="Error", description="Error when trying to retrieve data from https://8ball.delegator.com/magic/JSON/", color=0xff0000)
			embed.set_thumbnail(url='http://i.imgur.com/dx87cAe.png')
			embed.add_field(name="Reason", value=ex, inline=False)
			await dclient.say(embed=embed)
    else:
        await dclient.send_message(channel, '{}, **USAGE:** {}8ball <Question...>'.format(mention, cmd_char))
