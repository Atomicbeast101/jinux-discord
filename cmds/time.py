from config import CMD_CHAR
from datetime import datetime
from pytz import timezone, all_timezones


# Time command
async def ex(c, ch, m, a):
    if len(a) > 0:
        a = a.split(' ')[0]
        if len(a) == 3:
            a = a.upper()
        if a in all_timezones:
            t = datetime.now(timezone(a))
            await c.send_message(ch, 'It is `{:%H:%M:%S}` or `{:%I:%M:%S %p}` in `{}` right now.'.format(t, t, a))
        else:
            await c.send_message(ch, 'Invalid timezone input, `{}`! Please check <https://en.wikipedia.org/wiki/List_'
                                     'of_tz_database_time_zones>, {}!'.format(a, m))
    else:
        await c.send_message(ch, '{}, **USAGE:** {}time <timezone>'.format(m, CMD_CHAR))
