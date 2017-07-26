import aiohttp


# 8ball command
async def ex(dclient, channel, a, mention, cmd_char):
    if len(a.split(' ')) > 0:
        a.replace(' ', '+')
		try:
			async with aiohttp.ClientSession() as s:
				async with s.get('http://api.giphy.com/v1/gifs/random?api_key=dc6zaTOxFJmzC&tag={}'.format(a)) as r:
					d = await r.json()
					await dclient.send_message(channel, '{}'.format(d['data']['fixed_height_downsampled_url']))
		except Exception as e:
			embed=discord.Embed(title="Error", description="Error when trying to retrieve data from http://api.giphy.com/v1/gifs/random", color=0xff0000)
			embed.set_thumbnail(url='http://i.imgur.com/dx87cAe.png')
			embed.add_field(name="Reason", value=e.args[1], inline=False)
			await dclient.send_message(channel, embed=embed)
			return True, 'HTTP', 'Error when trying to retrieve data from http://api.giphy.com/v1/gifs/random. ERROR: {}'.format(e.args[1])
    else:
        await dclient.send_message(channel, '{}, **USAGE:** {}8ball <Question...>'.format(mention, cmd_char))
	return False
