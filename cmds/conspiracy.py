import random as r

# Conspiracy command
async def ex(dclient, channel, conspiracy_list):
    await dclient.send_message(channel, '{}'.format(r.choice(conspiracy_list)))
