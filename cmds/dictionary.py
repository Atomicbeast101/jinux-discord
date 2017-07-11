from PyDictionary import PyDictionary
import discord

# Dictionary command
async def ex(dclient, private_channel, public_channel, mention, a, cmd_char):
    a = a.split(' ')
    if len(a) == 1:
        word = a[0].lower()
        pydict = PyDictionary()
        r = pydict.meaning(word)

        # Creates embed for dictionary term
        embed = discord.Embed()
        embed.set_author(name='Meaning: {}'.format(word))
        embed.set_thumbnail(url='http://imgur.com/kqCrStG')
        try:
            if 'Noun' in r:
                cnt = 1
                val = ''
                for d in r['Noun']:
                    val += '''{}) {}
'''.format(cnt, d)
                embed.add_field(name='Noun', value=val)
            if 'Verb' in r:
                cnt = 1
                val = ''
                for d in r['Verb']:
                    val += '''{}) {}
'''.format(cnt, d)
                embed.add_field(name='Verb', value=val)
            if 'Adjective' in r:
                cnt = 1
                val = ''
                for d in r['Adjective']:
                    val += '''{}) {}
'''.format(cnt, d)
                embed.add_field(name='Adjective', value=val)

            # Send embed message to chat
            await dclient.send_message(private_channel, embed=embed)
            await dclient.send_message(public_channel, '{}, the meaning for the term `{}` has been sent in a private '
                                                       'message.'.format(mention, word))
        except Exception:
            await dclient.send_message(public_channel, '{}, there is no meaning for the term `{}`!'.format(mention,
                                                                                                           word))
    else:
        await dclient.send_message(public_channel, '{}, **USAGE:** {}dictionary <term>'.format(mention, cmd_char))
