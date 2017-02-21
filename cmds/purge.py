# Value Checker
def is_valid(m):
    try:
        int(m)
        return True
    except ValueError:
        return False


# Purge Command
async def ex(c, ch, m, a, Cmd_char):
    a = a.split(' ')
    if ch.permissions_for(ch).administrator:
        if len(a) == 1 and is_valid(a[0]):
            await c.purge_from(ch, int(a[0]))
            await c.send_message(ch, '{}, {} messages purged!'.format(m, a[0]))
        else:
            await c.send_message(ch, '{}, **USAGE** {}purge <#-of-messages>'.format(m, Cmd_char))
    else:
        await c.send_message(ch, '{}, you must be an administrator!'.format(m))
