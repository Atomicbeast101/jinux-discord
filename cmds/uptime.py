from datetime import datetime, timedelta


# Uptime command
async def ex(c, ch, ct):
    t = datetime.now() - ct
    f = datetime(1, 1, 1) + timedelta(seconds=t.seconds)
    await c.send_message(ch, 'I have been up for `{:d} days`, `{:d} hours`, `{:d} minutes`, and `{:d} seconds`'
                             '.'.format(f.day - 1, f.hour, f.minute, f.second))
