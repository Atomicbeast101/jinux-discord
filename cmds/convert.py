import aiohttp
from Data import CURR_LIST


# Value checker
def is_float(v):
    try:
        float(v)
        return True
    except ValueError:
        return False


# Convert command
async def ex(dclient, channel, mention, a, cmd_char):
    if len(a) == 3:
        b = a[0]
        cc = a[1].upper()
        ct = a[2].upper()
        if is_float(b):
            b = float(b)
            if cc in CURR_LIST and ct in CURR_LIST:
                async with aiohttp.ClientSession() as s:
                    async with s.get('http://free.currencyconverterapi.com/api/v3/convert?q={}_{}&compact=y'.format(
                            cc, ct)) as r:
                        d = await r.json()
                        nb = b * float(d[cc + '_' + ct]['val'])
                        await dclient.send_message(channel, '`{}: {:.2f}` > `{}: {:.2f}`'.format(cc, b, ct, nb))
            else:
                await dclient.send_message(channel, '{} Invalid currency code! Please check https://currencysystem.com/'
                                                    'codes/!'.format(mention))
        else:
            await dclient.send_message(channel, '{}, currency must be in numeric/decimal value! Like 100 or 54.42!'
                                       .format(mention))
    else:
        await dclient.send_message(channel, '{}, **USAGE:** {}convert <amount> <from-currency-code> <to-currency-code>'
                                   .format(mention, cmd_char))
