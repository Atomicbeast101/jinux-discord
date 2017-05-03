from translate import Translator
from Data import LANG_LIST


# Trans command
async def ex(dclient, channel, mention, a, cmd_char):
    ar = a.split(' ')
    if len(ar) >= 2:
        lang_id = ar[0]
        if lang_id.upper() in LANG_LIST:
            s = a[3:]
            t = Translator(to_lang=lang_id).translate(s)
            await dclient.send_message(channel, t)
        else:
            await dclient.send_message(channel, 'Invalid language code input, `{}`! Please check <https://www.'
                                                'sitepoint.com/web-foundations/iso-2-letter-language-codes/> '
                                                'for correct language code, {}!'.format(lang_id, mention))
    else:
        await dclient.send_message(channel, '{}, **USAGE:** {}trans <language-code> <to-translate>'.format(mention,
                                                                                                           cmd_char))
