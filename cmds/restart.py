import os, sys


async def ex(c, ch, m, au):
    if ch.permissions_for(au).administrator:
        await c.send_message(ch, ':regional_indicator_b: :regional_indicator_r: :regional_indicator_b:')
        os.execv(sys.executable, [sys.executable] + sys.argv)

        # This line only gets executed when the script hasn't restarted
        await c.send_message(ch, 'Something seems to have gone wrong.')
    else:
        await c.send_message(ch, 'You must be an administrator, {}!'.format(m))
