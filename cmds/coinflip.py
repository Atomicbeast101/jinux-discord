import random as r


# Coin flip command
async def ex(c, ch, m):
    await c.send_message(ch, '{}, coin says `{}`!'.format(m, r.choice(['heads', 'tails'])))
