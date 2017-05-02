import sqlite3
from time import localtime, strftime


# Custom command command
async def ex(dclient, channel, mention, author, a, cmd_list, con, con_ex, log_file, cmd_char):
    if channel.permissions_for(author):
        a = a.split(' ')
        if len(a) >= 2:
            cmd = a[0].lower()
            msg = ''
            for i in range(1, len(a)):
                msg += a[i] + ' '
            if len(cmd) > 10:
                await dclient.send_message(channel,
                                           '{}, command `{}` has `{}` characters. It must be 10 or less characters!'
                                           .format(mention, cmd, len(cmd)))
            else:
                if cmd in cmd_list:
                    await dclient.send_message(channel,
                                               '{}, command `{}` already exists! Please use a different command!'
                                               .format(mention, cmd))
                else:
                    try:
                        con_ex.execute("INSERT INTO custom_cmd VALUES (?, ?);", (cmd, msg))
                        con.commit()
                        cmd_list.append(cmd)
                        await dclient.send_message(channel, '{0}, command `{1}` made! Now just run `{2}{1}` to see the '
                                                            'message!'.format(mention, cmd, cmd_char))
                    except sqlite3.Error as e:
                        await dclient.send_message(channel,
                                                   '{}, error when trying to add info to database! Please notifiy '
                                                   'the admins!'.format(mention))
                        print('[{}]: {} - {}'.format(strftime("%b %d, %Y %X", localtime()), 'SQLITE',
                                                     'Error when trying to insert data: ' + e.args[0]))
                        log_file.write('[{}]: {} - {}\n'.format(strftime("%b %d, %Y %X", localtime()), 'SQLITE',
                                                                'Error when trying to insert data: ' + e.args[0]))
        else:
            await dclient.send_message(channel, '{}, **USAGE:** {}custcmd <cmd> <message...>'
                                       .format(mention, cmd_char))
    else:
        await dclient.send_message(channel, 'You must be an administrator, {}!'.format(mention))
    return cmd_list
