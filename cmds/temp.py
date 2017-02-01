# Value checker
def is_f(v):
    try:
        float(v)
        return True
    except ValueError:
        return False


# Temp command
async def ex(c, ch, m, a, CMD_CHAR):
    a = a.split(' ')
    if len(a) == 3:
        if is_f(a[0]):
            t = float(a[0])
            fr = a[1].upper()
            to = a[2].upper()
            if fr and to in ['F', 'K', 'C']:
                if fr == 'F' and to == 'K':
                    f = (t + 459.67) * (5 / 9)
                    await c.send_message(ch, '`{:.1f} Fahrenheit`  >  `{:.1f} Kelvin`'.format(t, f))
                elif fr == 'F' and to == 'C':
                    f = (t - 32) * .5556
                    await c.send_message(ch, '`{:.1f} Fahrenheit`  >  `{:.1f} Celsius`'.format(t, f))
                elif fr == 'K' and to == 'F':
                    f = (t * (9 / 5)) - 459.67
                    await c.send_message(ch, '`{:.1f} Kelvin`  >  `{:.1f} Fahrenheit`'.format(t, f))
                elif fr == 'K' and to == 'C':
                    f = (t * (9 / 5)) - 273.15
                    await c.send_message(ch, '`{:.1f} Kelvin`  >  `{:.1f} Celsius`'.format(t, f))
                elif fr == 'C' and to == 'F':
                    f = (t * 1.8) + 32
                    await c.send_message(ch, '`{:.1f} Celsius`  >  `{:.1f} Fahrenheit`'.format(t, f))
                elif fr == 'C' and to == 'K':
                    f = (t + 273.15) * (5 / 9)
                    await c.send_message(ch, '`{:.1f} Celsius`  >  `{:.1f} Kelvin`'.format(t, f))
            else:
                await c.send_message(ch, '{}, you must choose the option between `F`, `K`, or `C`!'.format(m))
        else:
            await c.send_message(ch, '{}, the temperature must be in numeric value (ex: 102 or 24.45)!'.format(m))
    else:
        await c.send_message(ch, '{}, **USAGE:** {}temp <#> <from F|K|C> <to F|K|C>'.format(m, CMD_CHAR))
