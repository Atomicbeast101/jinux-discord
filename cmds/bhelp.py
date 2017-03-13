from Data import *


# Help command
async def ex(dclient, private_channel, public_channel, mention, a, cmd_char):
    if len(a) == 2:
        s = a[1].lower()
        s.replace(cmd_char, '')
        if s == 'cat':
            await dclient.send_message(public_channel, HELP_CAT)
        elif s == 'channelinfo':
            await dclient.send_message(public_channel, HELP_CHANNELINFO)
        elif s == 'choose':
            await dclient.send_message(public_channel, HELP_CHOOSE)
        elif s == 'chucknorris':
            await dclient.send_message(public_channel, HELP_CHUCKNORRIS)
        elif s == 'coinflip':
            await dclient.send_message(public_channel, HELP_COINFLIP)
        elif s == 'convert':
            await dclient.send_message(public_channel, HELP_CONVERT)
        elif s == 'dice':
            await dclient.send_message(public_channel, HELP_DICE)
        elif s == 'dictionary':
            await dclient.send_message(public_channel, HELP_DICTIONARY)
        elif s == '8ball':
            await dclient.send_message(public_channel, HELP_EIGHTBALL)
        elif s == 'gif':
            await dclient.send_message(public_channel, HELP_GIF)
        elif s == 'info':
            await dclient.send_message(public_channel, HELP_INFO)
        elif s == 'poll':
            await dclient.send_message(public_channel, HELP_POLL)
        elif s == 'reddit':
            await dclient.send_message(public_channel, HELP_REDDIT)
        elif s == 'rps':
            await dclient.send_message(public_channel, HELP_RPS)
        elif s == 'serverinfo':
            await dclient.send_message(public_channel, HELP_SERVERINFO)
        elif s == 'temp':
            await dclient.send_message(public_channel, HELP_TEMP)
        elif s == 'time':
            await dclient.send_message(public_channel, HELP_TIME)
        elif s == 'trans':
            await dclient.send_message(public_channel, HELP_TRANS)
        elif s == 'twitch':
            await dclient.send_message(public_channel, HELP_TWITCH)
        elif s == 'update':
            await dclient.send_message(public_channel, HELP_UDPATE)
        elif s == 'uptime':
            await dclient.send_message(public_channel, HELP_UPTIME)
        elif s == 'xkcd':
            await dclient.send_message(public_channel, HELP_XKCD)
        elif s == 'youtube':
            await dclient.send_message(public_channel, HELP_YOUTUBE)
        elif s == '9':
            await dclient.send_message(public_channel, HELP_NINE)
        else:
            await dclient.send_message(public_channel, 'I am unable to find the command you are looking for, {}! '
                                                       'Perhaps check {}help?'.format(mention, cmd_char))
    else:
        await dclient.send_message(private_channel, HELP)
        await dclient.send_message(public_channel, '{}, I sent you the help guide in a private message.'.format(mention))
