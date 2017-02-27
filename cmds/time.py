from datetime import datetime
from pytz import timezone, all_timezones


# Time command
async def ex(dclient, channel, mention, a, cmd_char):
    if len(a) > 0:
        a = a.split(' ')[0]
        if len(a) == 3:
            a = a.upper()
        if a in all_timezones:
            time_now = datetime.now(timezone(a))
            await dclient.send_message(channel, 'It is `{:%H:%M:%S}` or `{:%I:%M:%S %p}` in `{}` right now.'
                                       .format(time_now, time_now, a))
        else:
            await dclient.send_message(channel, 'Invalid timezone input, `{}`! Please check <https://en.wikipedia.org'
                                                '/wiki/List_of_tz_database_time_zones>, {}!'.format(a, mention))
    else:
        await dclient.send_message(channel, '{}, **USAGE:** {}time <timezone>'.format(mention, cmd_char))
