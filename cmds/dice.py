import random as r


# Dice command
async def ex(c, ch, m):
    await c.send_message(ch, '{}, *rolls dice...* I got a `{}`!'.format(m, r.choice(['1', '2', '3', '4', '5', '6'])))
