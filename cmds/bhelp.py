from Data import *


# Help command
async def ex(dclient, private_channel, public_channel, mention, a, cmd_char):
    if len(a) == 2:
        cmd = a[1].lower()
        cmd.replace(cmd_char, '')
        if(cmd in HELP_CMD.keys()):
            await dclient.send_message(private_channel, HELP_CMD[cmd])
            await dclient.send_message(public_channel, '{}, I sent you the specific help guide in a private message.'
                                       .format(mention))
        else:
            await dclient.send_message(public_channel, 'I am unable to find the command you are looking for, {}! '
                                                       'Perhaps check {}help?'.format(mention, cmd_char))

    else:
        await dclient.send_message(private_channel, HELP)
        await dclient.send_message(private_channel, HELP2)
        await dclient.send_message(public_channel, '{}, I sent you the help guide in a private message.'
                                   .format(mention))
