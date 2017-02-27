from PyDictionary import PyDictionary

# Dictionary command
async def ex(dclient, private_channel, public_channel, mention, a, cmd_char):
    a = a.split(' ')
    if len(a) == 1:
        word = a[0].lower()
        pydict = PyDictionary()
        r = pydict.meaning(word)
        try:
            an = '''```Markdown
# Meaning: {} #
'''.format(word)
            if 'Noun' in r:
                an += '''<Noun>
'''
                cnt = 1
                for d in r['Noun']:
                    an += '''[{}]: {}
'''.format(cnt, d)
                    cnt += 1
            if 'Verb' in r:
                an += '''<Verb>
'''
                cnt = 1
                for d in r['Verb']:
                    an += '''[{}]: {}
'''.format(cnt, d)
                    cnt += 1
            if 'Adjective' in r:
                an += '''<Adjective>
'''
                cnt = 1
                for d in r['Adjective']:
                    an += '''[{}]: {}
'''.format(cnt, d)
                    cnt += 1
            an += '''```'''
            await dclient.send_message(private_channel, an)
            await dclient.send_message(public_channel, '{}, the meaning for the term `{}` has been sent in a private '
                                                       'message.'.format(mention, word))
        except Exception:
            await dclient.send_message(public_channel, '{}, there is no meaning for the term `{}`!'.format(mention,
                                                                                                           word))
    else:
        await dclient.send_message(public_channel, '{}, **USAGE:** {}dictionary <term>'.format(mention, cmd_char))
