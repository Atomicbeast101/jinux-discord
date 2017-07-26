import random as r


# Choose command
async def ex(dclient, channel, mention, a, cmd_char):
    options = a.split(' ')
    if len(options) >= 2:
        await dclient.send_message(channel, '{}, I choose `{}`!'.format(mention, r.choice(options)))
        return None
    else:
        msg = await dclient.send_message(channel, '{}, **USAGE:** {}choose <options>. Must be two options or more (ex: '
                                                  '-choose red green)!'.format(mention, cmd_char))
        return msg
