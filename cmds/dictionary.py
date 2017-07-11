from PyDictionary import PyDictionary

# Dictionary command
async def ex(dclient, private_channel, public_channel, mention, a, cmd_char):
    a = a.split(' ')
    if len(a) == 1:
        word = a[0].lower()
        pydict = PyDictionary()
        r = pydict.meaning(word)
        try:
			word_type = ''
			noun_means = ''
			verb_means = ''
			adj_means = ''
			
			# Retrieve noun meanings
            if 'Noun' in r:
				word_type += 'Noun'
				count = 1
				for d in r['Noun']:
					noun_means += '''```[{}]: {}
'''.format(count, d)
				count += 1
				if count == 3:
					noun_means += '''```'''
					break
			
			# Retrieve verb meanings
            if 'Verb' in r:
				if 'Noun' in word_type:
					word_type += '/Verb'
				count = 1
				for d in r['Verb']:
					verb_means += '''```[{}]: {}
'''.format(count, d)
					count += 1
					if count == 3:
						verb_means += '''```'''
						break
			
			# Retrieve adjective meanings
            if 'Adjective' in r:
				if 'Noun' in word_type or 'Verb' in word_type:
					word_type += '/Adjective'
				count = 1
				for d in r['Adjective']:
					adj_means += '''```[{}]: {}
'''.format(count, d)
					count += 1
					if count == 3:
						adj_means += '''```'''
						break
			
			# Create embed object
			embed=discord.Embed(title=word, description=word_type, color=0xff8000)
			embed.set_thumbnail(url='http://i.imgur.com/I1EtOLU.png')
			if 'Noun' in word_type:
				embed.add_field(name='Noun', value=noun_means, inline=False)
			if 'Verb' in word_type:
				embed.add_field(name='Verb', value=verb_means, inline=False)
			if 'Adjective' in word_type:
				embed.add_field(name='Adjective', value=adj_means, inline=False)
			
            await dclient.send_message(private_channel, embed=embed)
            await dclient.send_message(public_channel, '{}, the meaning for the term `{}` has been sent in a private '
                                                       'message.'.format(mention, word))
        except Exception:
            await dclient.send_message(public_channel, '{}, there is no meaning for the term `{}`!'.format(mention,
                                                                                                           word))
    else:
        await dclient.send_message(public_channel, '{}, **USAGE:** {}dictionary <term>'.format(mention, cmd_char))
