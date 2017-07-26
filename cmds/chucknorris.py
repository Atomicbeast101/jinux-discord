import aiohttp


# Chuck Norris command
async def ex(dclient, channel):
	try:
		async with aiohttp.ClientSession() as s:
			async with s.get('https://api.chucknorris.io/jokes/random') as r:
				d = await r.json()
				await dclient.send_message(channel, '{}'.format(d['value']))
	except Exception as e:
		embed=discord.Embed(title="Error", description="Error when trying to retrieve data from https://api.chucknorris.io/jokes/random", color=0xff0000)
		embed.set_thumbnail(url='http://i.imgur.com/dx87cAe.png')
		embed.add_field(name="Reason", value=e.args[1], inline=False)
		msg = await dclient.send_message(channel, embed=embed)
		return True, 'HTTP', 'Error when trying to retrieve data from https://api.chucknorris.io/jokes/random. ERROR: {}'.format(e.args[1]), msg
	return False, None, None, None
