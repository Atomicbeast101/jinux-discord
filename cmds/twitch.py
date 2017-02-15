from configparser import ConfigParser


# Twitch command
async def ex(c, pch, dch, m, a, tw_en, ch_id, users, active, cmd_char):
    a = a.split(' ')
    if len(a) >= 1:
        sc = a[0].lower()
        if sc == 'add':
            if dch.permissions_for(pch).administrator:
                if len(a) == 2 and a[1] != '':
                    u = a[1].lower()
                    if u in users:
                        await c.send_message(dch, '{}, `{}` is already in the list!'.format(m, u))
                    else:
                        users.append(u)
                        config = ConfigParser()
                        config.read('config.ini')
                        config.set('Twitch', 'Users', ','.join(users))
                        with open('config.ini', 'w') as configfile:
                            config.write(configfile)
                        await c.send_message(dch, '{}, `{}` added!'.format(m, u))
                else:
                    await c.send_message(dch, '{}, **USAGE** {}twitch add <username>'.format(m, cmd_char))
            else:
                await c.send_message(dch, '{}, you must be an administrator!'.format(m))
        elif sc == 'remove':
            if dch.permissions_for(pch).administrator:
                if len(a) == 2:
                    u = a[1].lower()
                    if u in users:
                        users.remove(u)
                        config = ConfigParser()
                        config.read('config.ini')
                        config.set('Twitch', 'Users', ','.join(users))
                        with open('config.ini', 'w') as configfile:
                            config.write(configfile)
                        await c.send_message(dch, '{}, `{}` removed!'.format(m, u))
                    else:
                        await c.send_message(dch, '{}, `{}` is not in the list!'.format(m, u))
                else:
                    await c.send_message(dch, '{}, **USAGE** {}twitch remove <username>'.format(m, cmd_char))
            else:
                await c.send_message(dch, '{}, you must be an administrator!'.format(m))
        elif sc == 'list':
            if tw_en:
                if len(users) > 0:
                    await c.send_message(pch, 'List of Twitch usernames: ```{}```'.format(', '.join(users)))
                    await c.send_message(dch, '{}, list of Twitch usernames has been sent in a private channel.'.format(m))
                else:
                    await c.send_message(dch, '{}, there are no usernames in the list!'.format(m))
            else:
                await c.send_message(dch, '{}, Twitch notification is not enabled!'.format(m))
        elif sc == 'toggle':
            if dch.permissions_for(pch).administrator:
                if tw_en:
                    tw_en = False
                else:
                    tw_en = True
                config = ConfigParser()
                config.read('config.ini')
                config.set('Twitch', 'Enabled', str(tw_en))
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
                await c.send_message(dch, '{}, Twitch live status notification is now set to `{}`!'.format(m,
                                                                                                           str(tw_en)))
            else:
                await c.send_message(dch, '{}, you must be an administrator!'.format(m))
        elif sc == 'setchannel':
            if dch.permissions_for(pch).administrator:
                ch_id = dch.id
                config = ConfigParser()
                config.read('config.ini')
                config.set('Twitch', 'Channel', ch_id)
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
                await c.send_message(dch, '{}, it is now set! The notifications will appear here!'.format(m))
            else:
                await c.send_message(dch, '{}, you must be an administrator!'.format(m))
        else:
            await c.send_message(dch, '{}, **USAGE:** {}twitch <add|remove|list|toggle|setchannel>'.format(m, cmd_char))
    else:
        await c.send_message(dch, '{}, **USAGE:** {}twitch <add|remove|list|toggle|setchannel>'.format(m, cmd_char))
    return tw_en, ch_id, users, active
