import random as r


# Coin flip command
async def ex(dclient, channel, mention):
    await dclient.send_message(channel, '{}, coin says `{}`!'.format(mention, r.choice(['heads', 'tails'])))
