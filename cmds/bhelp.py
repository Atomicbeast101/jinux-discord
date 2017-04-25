from Data import *


# Help command
async def ex(dclient, private_channel, public_channel, mention, a, cmd_char):
    if len(a) == 2:
        s = a[1].lower()
        s.replace(cmd_char, '')
        if s == 'cat':
            await dclient.send_message(private_channel, HELP_CAT)
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        elif s == 'channelinfo':
            await dclient.send_message(private_channel, HELP_CHANNELINFO)
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        elif s == 'choose':
            await dclient.send_message(private_channel, HELP_CHOOSE)
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        elif s == 'chucknorris':
            await dclient.send_message(private_channel, HELP_CHUCKNORRIS)
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        elif s == 'coinflip':
            await dclient.send_message(private_channel, HELP_COINFLIP)
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        elif s == 'conspiracy':
            await dclient.send_message(private_channel, HELP_CONSPIRACY)
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        elif s == 'custcmd':
            await dclient.send_message(private_channel, HELP_CUSTCMD)
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        elif s == 'convert':
            await dclient.send_message(private_channel, HELP_CONVERT)
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        elif s == 'dice':
            await dclient.send_message(private_channel, HELP_DICE)
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        elif s == 'dictionary':
            await dclient.send_message(private_channel, HELP_DICTIONARY)
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        elif s == '8ball':
            await dclient.send_message(private_channel, HELP_EIGHTBALL)
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        elif s == 'gif':
            await dclient.send_message(private_channel, HELP_GIF)
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        elif s == 'info':
            await dclient.send_message(private_channel, HELP_INFO)
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        elif s == 'poll':
            await dclient.send_message(private_channel, HELP_POLL)
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        elif s == 'reddit':
            await dclient.send_message(private_channel, HELP_REDDIT)
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        elif s == 'remindall':
            await dclient.send_message(private_channel, HELP_REMINDALL)
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        elif s == 'remindme':
            await dclient.send_message(private_channel, HELP_REMINDME)
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        elif s == 'rps':
            await dclient.send_message(private_channel, HELP_RPS)
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        elif s == 'serverinfo':
            await dclient.send_message(private_channel, HELP_SERVERINFO)
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        elif s == 'temp':
            await dclient.send_message(private_channel, HELP_TEMP)
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        elif s == 'time':
            await dclient.send_message(private_channel, HELP_TIME)
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        elif s == 'trans':
            await dclient.send_message(private_channel, HELP_TRANS)
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        elif s == 'twitch':
            await dclient.send_message(private_channel, HELP_TWITCH)
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        elif s == 'uptime':
            await dclient.send_message(private_channel, HELP_UPTIME)
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        elif s == 'xkcd':
            await dclient.send_message(private_channel, HELP_XKCD)
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        elif s == 'youtube':
            await dclient.send_message(private_channel, HELP_YOUTUBE)
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        else:
            await dclient.send_message(public_channel, 'I am unable to find the command you are looking for, {}! '
                                                       'Perhaps check {}help?'.format(mention, cmd_char))

    else:
        await dclient.send_message(private_channel, HELP)
        await dclient.send_message(public_channel, '{}, I sent you the help guide in a private message.'
                                   .format(mention))
