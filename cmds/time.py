from datetime import datetime
from geopy import geocoders


# Time command
async def ex(dclient, channel, mention, a, cmd_char):
    if len(a) > 0:
        g = geocoders.GoogleV3()
        try:
            place, (lat, lng) = g.geocode(a)
            timezone = g.timezone((lat, lng))
            time_now = datetime.now(timezone)
            await dclient.send_message(channel, 'It is `{:%H:%M:%S}` or `{:%I:%M:%S %p}` in `{}` right now.'
                                       .format(time_now, time_now, a))
        except Exception:
            await dclient.send_message(channel, 'Location `{}` unknown! Please try to be more specific! I rely on '
                                                'Google maps to get the coordinates for the timezone, {}!'
                                       .format(a, mention))
    else:
        await dclient.send_message(channel, '{}, **USAGE:** {}time <timezone>'.format(mention, cmd_char))
