import aiohttp


# 8ball command
async def ex(dclient, channel, mention, question, cmd_char):
	msg = None
    if len(question.split(' ')) >= 1:
        question.replace(' ', '%')
        question.replace('?', '%3F')
        question.replace(',', '%2C')
		try:
			async with aiohttp.ClientSession() as s:
				async with s.get('https://8ball.delegator.com/magic/JSON/{}'.format(question)) as r:
					d = await r.json()
					await dclient.send_message(channel, '{}, {}'.format(mention, d['magic']['answer']))
		except Exception as e:
			embed=discord.Embed(title="Error", description="Error when trying to retrieve data from https://8ball.delegator.com/magic/JSON/", color=0xff0000)
			embed.set_thumbnail(url='http://i.imgur.com/dx87cAe.png')
			embed.add_field(name="Reason", value=e.args[1], inline=False)
			msg = await dclient.send_message(channel, embed=embed)
			return True, 'HTTP', 'Error when trying to retrieve data from https://8ball.delegator.com/magic/JSON/. ERROR: {}'.format(e.args[1]), msg
    else:
        msg = await dclient.send_message(channel, '{}, **USAGE:** {}8ball <Question...>'.format(mention, cmd_char))
	return False, None, None, msg
