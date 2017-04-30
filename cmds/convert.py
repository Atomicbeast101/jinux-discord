import aiohttp
import re
from Data import CURR_LIST


# Value checker
def is_money_value(v):
    try:
        val = float(v)
        return val
    except ValueError:
        if re.match('[0-9]+[bmk$]', v):
            return True
        else:
            return False


# Convert to float
def get_money_value(v):
    try:
        val = float(v)
        return val
    except ValueError:
        if re.match('[0-9]+[bmk$]', v):
            if 'b' in v:
                if v.count('b') > 1:
                    to_remove = v.count('b')
                    v = v[:to_remove]
                val = float(v)
                return val
            elif 'm' in v:
                if v.count('b') > 1:
                    to_remove = v.count('b')
                    v = v[:to_remove]
                val = float(v)
                return val
            if 'k' in v:
                if v.count('b') > 1:
                    to_remove = v.count('b')
                    v = v[:to_remove]
                val = float(v)
                return val
        else:
            return False


# Convert command
async def ex(dclient, channel, mention, a, cmd_char):
    if len(a) == 3:
        b = a[0]
        cc = a[1].upper()
        ct = a[2].upper()
        if is_money_value(b):
            b = get_money_value(b)
            if cc and ct in CURR_LIST:
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
