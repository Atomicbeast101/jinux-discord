from configparser import ConfigParser


# Twitch command
async def ex(dclient, private_channel, public_channel, mention, a, twitch_enable, twitch_channel_id, users, active,
             cmd_char):
    msg = None
    a = a.split(' ')
    if len(a) >= 1:
        sc = a[0].lower()
        if sc == 'add':
            if public_channel.permissions_for(private_channel).administrator:
                if len(a) == 2 and a[1] != '':
                    u = a[1].lower()
                    if u in users:
                        msg = await dclient.send_message(public_channel, '{}, `{}` is already in the list!'.format(mention,
                                                                                                             u))
                    else:
                        users.append(u)
                        config = ConfigParser()
                        config.read('config.ini')
                        config.set('Twitch', 'Users', ','.join(users))
                        with open('config.ini', 'w') as configfile:
                            config.write(configfile)
                        msg = await dclient.send_message(public_channel, '{}, `{}` added!'.format(mention, u))
                else:
                    msg = await dclient.send_message(public_channel, '{}, **USAGE** {}twitch add <username>'.format(mention,
                                                                                                              cmd_char))
            else:
                msg = await dclient.send_message(public_channel, '{}, you must be an administrator!'.format(mention))
        elif sc == 'remove':
            if public_channel.permissions_for(private_channel).administrator:
                if len(a) == 2:
                    u = a[1].lower()
                    if u in users:
                        users.remove(u)
                        config = ConfigParser()
                        config.read('config.ini')
                        config.set('Twitch', 'Users', ','.join(users))
                        with open('config.ini', 'w') as configfile:
                            config.write(configfile)
                        msg = await dclient.send_message(public_channel, '{}, `{}` removed!'.format(mention, u))
                    else:
                        msg = await dclient.send_message(public_channel, '{}, `{}` is not in the list!'.format(mention, u))
                else:
                    msg = await dclient.send_message(public_channel, '{}, **USAGE** {}twitch remove <username>'
                                               .format(mention, cmd_char))
            else:
                msg = await dclient.send_message(public_channel, '{}, you must be an administrator!'.format(mention))
        elif sc == 'list':
            if twitch_enable:
                if len(users) > 0:
                    await dclient.send_message(private_channel, 'List of Twitch usernames: ```{}```'.format(
                        ', '.join(users)))
                    msg = await dclient.send_message(public_channel, '{}, list of Twitch usernames has been sent in a '
                                                               'private channel.'.format(mention))
                else:
                    msg = await dclient.send_message(public_channel, '{}, there are no usernames in the list!'
                                               .format(mention))
            else:
                msg = await dclient.send_message(public_channel, '{}, Twitch notification is not enabled!'.format(mention))
        elif sc == 'toggle':
            if public_channel.permissions_for(private_channel).administrator:
                if twitch_enable:
                    twitch_enable = False
                else:
                    twitch_enable = True
                config = ConfigParser()
                config.read('config.ini')
                config.set('Twitch', 'Enabled', str(twitch_enable))
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
                msg = await dclient.send_message(public_channel, '{}, Twitch live status notification is now set to `{}`!'
                                           .format(mention, str(twitch_enable)))
            else:
                await dclient.send_message(public_channel, '{}, you must be an administrator!'.format(mention))
        elif sc == 'setchannel':
            if public_channel.permissions_for(private_channel).administrator:
                twitch_channel_id = public_channel.id
                config = ConfigParser()
                config.read('config.ini')
                config.set('Twitch', 'Channel', twitch_channel_id)
                with open('config.ini', 'w') as configfile:
                    config.write(configfile)
                msg = await dclient.send_message(public_channel, '{}, it is now set! The notifications will appear here!'
                                           .format(mention))
            else:
                msg = await dclient.send_message(public_channel, '{}, you must be an administrator!'.format(mention))
        else:
            msg = await dclient.send_message(public_channel, '{}, **USAGE:** {}twitch <add|remove|list|toggle|setchannel>'
                                       .format(mention, cmd_char))
    else:
        msg = await dclient.send_message(public_channel, '{}, **USAGE:** {}twitch <add|remove|list|toggle|setchannel>'
                                   .format(mention, cmd_char))
    return twitch_enable, twitch_channel_id, users, active, msg
