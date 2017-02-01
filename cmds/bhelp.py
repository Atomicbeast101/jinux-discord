from Data import *


# Help command
async def ex(c, pch, dch, m, a, CMD_CHAR):
    if len(a) == 2:
        s = a[1].lower()
        s.replace(CMD_CHAR, '')
        if s == 'cat':
            await c.send_message(dch, HELP_CAT)
        elif s == 'choose':
            await c.send_message(dch, HELP_CHOOSE)
        elif s == 'chucknorris':
            await c.send_message(dch, HELP_CHUCKNORRIS)
        elif s == 'coinflip':
            await c.send_message(dch, HELP_COINFLIP)
        elif s == 'convert':
            await c.send_message(dch, HELP_CONVERT)
        elif s == 'dice':
            await c.send_message(dch, HELP_DICE)
        elif s == '8ball':
            await c.send_message(dch, HELP_EIGHTBALL)
        elif s == 'gif':
            await c.send_message(dch, HELP_GIF)
        elif s == 'info':
            await c.send_message(dch, HELP_INFO)
        elif s == 'poll':
            await c.send_message(dch, HELP_POLL)
        elif s == 'purge':
            await c.send_message(dch, HELP_PURGE)
        elif s == 'reddit':
            await c.send_message(dch, HELP_REDDIT)
        elif s == 'rps':
            await c.send_message(dch, HELP_RPS)
        elif s == 'temp':
            await c.send_message(dch, HELP_TEMP)
        elif s == 'time':
            await c.send_message(dch, HELP_TIME)
        elif s == 'trans':
            await c.send_message(dch, HELP_TRANS)
        elif s == 'twitch':
            await c.send_message(dch, HELP_TWITCH)
        elif s == 'uptime':
            await c.send_message(dch, HELP_UPTIME)
        elif s == 'xkcd':
            await c.send_message(dch, HELP_XKCD)
        elif s == 'youtube':
            await c.send_message(dch, HELP_YOUTUBE)
        else:
            await c.send_message(dch, 'I am unable to find the command you are looking for, {}! Perhaps check {}help'
                                      '?'.format(m, CMD_CHAR))
    else:
        await c.send_message(pch, HELP)
        await c.send_message(dch, '{}, I sent you the help guide in a private message.'.format(m))
