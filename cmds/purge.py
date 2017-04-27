import discord


# Value Checker
def is_valid(m):
    try:
        int(m)
        return True
    except ValueError:
        return False


# Purge Command
async def ex(dclient, channel, author, mention, a, cmd_char):
    a = a.split(' ')
    if channel.permissions_for(author):
        try:
            if len(a) == 1 and is_valid(a[0]):
                purge_limit = int(a[0])
                if 2 <= purge_limit <= 100:
                    msgs = list()
                    async for msg in dclient.logs_from(channel, limit=purge_limit):
                        msgs.append(msg)
                    await dclient.delete_messages(msgs)
                    await dclient.send_message(channel, '{}, `{}` messages has been removed from this channel.'
                                               .format(mention, purge_limit))
                else:
                    await dclient.send_message(channel, '{}, you can only delete messages between `2` and `100`!'
                                               .format(mention))
            else:
                await dclient.send_message(channel, '{}, **USAGE** {}purge <#-of-messages>'.format(mention, cmd_char))
        except discord.Forbidden:
            await dclient.send_message(channel, "{}, I don't have access to `manage_messages`! Please notify an "
                                                "admin!".format(mention))
    else:
        await dclient.send_message(channel, '{}, you must be an administrator!'.format(mention))
