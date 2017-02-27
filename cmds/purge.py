# Value Checker
def is_valid(m):
    try:
        int(m)
        return True
    except ValueError:
        return False


# Purge Command
async def ex(dclient, channel, mention, a, cmd_char):
    a = a.split(' ')
    if channel.permissions_for(a).administrator:
        if len(a) == 1 and is_valid(a[0]):
            await dclient.purge_from(channel, int(a[0]))
            await dclient.send_message(channel, '{}, {} messages purged!'.format(mention, a[0]))
        else:
            await dclient.send_message(channel, '{}, **USAGE** {}purge <#-of-messages>'.format(mention, cmd_char))
    else:
        await dclient.send_message(channel, '{}, you must be an administrator!'.format(mention))
