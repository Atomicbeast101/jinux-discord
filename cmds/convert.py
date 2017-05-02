import aiohttp
import re
from Data import CURR_LIST


# Count # of letters in money value
def num_letters(v):
    count = 0
    for char in v:
        if char.isalpha():
            count += 1
    return count


# Value checker
def is_money_value(v):
    try:
        val = float(v)
        return val
    except ValueError:
        if re.match('[0-9]+[bmk$]', v) and num_letters(v) <= 1:
            return True
        else:
            return False


# Convert to float
def get_money_value(v):
    try:
        val = float(v)
        return val
    except ValueError:
        if 'b' in v:
            v = v[:-1]
            val = float(v) * 1000000000
            return val
        elif 'm' in v:
            v = v[:-1]
            val = float(v) * 1000000
            return val
        if 'k' in v:
            v = v[:-1]
            val = float(v) * 1000
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
                        await dclient.send_message(channel, '`{}: {:,.2f}` > `{}: {:,.2f}`'.format(cc, b, ct, nb))
            else:
                await dclient.send_message(channel, '{} Invalid currency code! Please check https://currencysystem.com/'
                                                    'codes/!'.format(mention))
        else:
            await dclient.send_message(channel, '{}, currency must be in numeric/decimal value (ex: `100` or `54.42`) '
                                                'or must be in #type format (ex: `1m` = 1 million or `2k` = 2 thousand '
                                                'or `5b` = 5 billion)!'.format(mention))
    else:
        await dclient.send_message(channel, '{}, **USAGE:** {}convert <amount> <from-currency-code> <to-currency-code>'
                                   .format(mention, cmd_char))
