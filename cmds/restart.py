import os
import sys

# Restart command
async def ex(dclient, channel, mention, au):
    if channel.permissions_for(au).administrator:
        await dclient.send_message(channel, ':sleeping:')
        os.execv(sys.executable, [sys.executable] + sys.argv)

        # This line only gets executed when the script hasn't restarted
        await dclient.send_message(channel, 'Something seems to have gone wrong.')
    else:
        await dclient.send_message(channel, 'You must be an administrator, {}!'.format(mention))
