import random as r


# Choose command
async def ex(c, ch, m, o, CMD_CHAR):
    if len(o) >= 2:
        await c.send_message(ch, '{}, I choose `{}`!'.format(m, r.choice(o)))
    else:
        await c.send_message(ch, '{}, **USAGE:** {}choose <options>. Must be two options or more (ex: -choose red '
                                 'green)!'.format(m, CMD_CHAR))
