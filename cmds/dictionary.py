from PyDictionary import PyDictionary
import json

# Dictionary command
async def ex(c, pch, dch, m, a, Cmd_char):
    a = a.split(' ')
    if len(a) == 1:
        wrd = a[0].lower()
        pydict = PyDictionary()
        r = json.loads(pydict.meaning(wrd))
        an = '''```Apache
# Definition: {} #'''.format(wrd)
        if 'Noun' in r:
            an += '''Noun
'''
            cnt = 1
            for d in r['Noun']:
                an += '''  {}) {}
'''.format(cnt, d)
                cnt += 1
        if 'Verb' in r:
            an += '''Verb
'''
            cnt = 1
            for d in r['Verb']:
                an += '''  {}) ()
'''.format(cnt, d)
                cnt += 1
        if 'Adjective' in r:
            an += '''Adjective
            '''
            cnt = 1
            for d in r['Adjective']:
                an += '''  {}) ()
            '''.format(cnt, d)
                cnt += 1
        an += '''```'''
        await c.send_message(pch, an)
        await c.send_message(dch, '{}, the meaning for the term `{}` has been sent in a private message.'
                             .format(m, wrd))
    else:
        await c.send_message(dch, '{}, **USAGE:** {}dictionary <term>'.format(m, Cmd_char))
