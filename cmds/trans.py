import aiohttp
from translate import Translator
from Data import LANG_LIST


# Trans command
async def ex(c, ch, m, a, CMD_CHAR):
    if len(a.split(' ')) >= 2:
        if a.split(' ')[0].upper() in LANG_LIST:
            s = a[3:]
            t = Translator(to_lang=a.split(' ')[0]).translate(s)
            await c.send_message(ch, t)
        else:
            await c.send_message(ch, 'Invalid language code input, `{}`! Please check <https://www.sitepoint.com/web-'
                                     'foundations/iso-2-letter-language-codes/> for correct language code, {}!'
                                 .format(a[0], m))
    else:
        await c.send_message(ch, '{}, **USAGE:** {}trans <language-code> <to-translate>'.format(m, CMD_CHAR))
