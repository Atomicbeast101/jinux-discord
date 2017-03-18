import random as r


# Dice command
async def ex(dclient, channel, mention):
    await dclient.send_message(channel, '{}, *rolls dice...* I got a `{}`!'
                               .format(mention, r.choice(['1', '2', '3', '4', '5', '6'])))
