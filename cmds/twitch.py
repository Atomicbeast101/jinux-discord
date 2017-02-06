from configparser import ConfigParser


# Twitch command
async def ex(c, pch, dch, m, a, tw_en, ch_id, users, active, CMD_CHAR):
    a = a.split(' ')
    if len(a) > 0:
        sc = a[0].lower()
        if sc == 'add':
            if dch.permissions_for(pch).administrator:
                if len(a) == 2:
                    u = a[1].lower()
                    if u in users:
                        await c.send_message(c, '{}, `{}` is already in the list!'.format(m, u))
                    else:
                        users.append(u)
                        config = ConfigParser()
                        config.set('Twitch', 'users', users)
                        await c.send_message(dch, '{}, `{}` added!'.format(m, u))
                else:
                    await c.send_message(dch, '{}, **USAGE** {}twitch add <username>'.format(m, CMD_CHAR))
            else:
                await c.send_message(dch, '{}, you must be an administrator!'.format(m))
        elif sc == 'remove':
            if dch.permissions_for(pch).administrator:
                if len(a) == 2:
                    u = a[1].lower()
                    if u in users:
                        users.remove(u)
                        config = ConfigParser()
                        config.set('Twitch', 'users', users)
                        await c.send_message(dch, '{}, `{}` removed!'.format(m, u))
                    else:
                        await c.send_message(dch, '{}, `{}` is not in the list!'.format(m, u))
                else:
                    await c.send_message(dch, '{}, **USAGE** {}twitch remove <username>'.format(m,
                                                                                              CMD_CHAR))
            else:
                await c.send_message(dch, '{}, you must be an administrator!'.format(m))
        elif sc == 'list':
            await c.send_message(pch, 'List of Twitch usernames: ```{}```'
                                 .format(', '.join(str(u) for u in users)))
            await c.send_message(dch, '{}, list of Twitch usernames has been sent in a private channe'
                                      'l.'.format(m))
        elif sc == 'toggle':
            if dch.permissions_for(pch).administrator:
                if tw_en:
                    tw_en = False
                else:
                    tw_en = True
                config = ConfigParser()
                config.set('Twitch', 'enable', tw_en)
                await c.send_message(dch, '{}, Twitch live status notification is now set to `{}`!'.format(m,
                                                                                                           str(tw_en)))
            else:
                await c.send_message(dch, '{}, you must be an administrator!'.format(m))
        elif sc == 'setchannel':
            if dch.permissions_for(pch).administrator:
                ch_id = dch.id
                config = ConfigParser()
                config.set('Twitch', 'channel', ch_id)
                await c.send_message(dch, '{}, it is now set! The notifications will appear here!'.format(m))
            else:
                await c.send_message(dch, '{}, you must be an administrator!'.format(m))
    else:
        await c.send_message(dch, '{}, **USAGE:** {}twitch <add|remove|list|toggle|setchannel>'.format(m, CMD_CHAR))
    return tw_en, ch_id, users, active
