import sqlite3
from time import localtime, strftime


# Custom command command
async def ex(dclient, channel, mention, author, a, cmd_list, con, con_ex, log_file, cmd_char):
    msg = None
    if channel.permissions_for(author):
        a = a.split(' ')
        if len(a) >= 2:
            cmd = a[0].lower()
            msg = ''
            for i in range(1, len(a)):
                msg += a[i] + ' '
            if len(cmd) > 10:
                msg = await dclient.send_message(channel,
                                           '{}, command `{}` has `{}` characters. It must be 10 or less characters!'
                                           .format(mention, cmd, len(cmd)))
            else:
                if cmd in cmd_list:
                    msg = await dclient.send_message(channel,
                                               '{}, command `{}` already exists! Please use a different command!'
                                               .format(mention, cmd))
                else:
                    try:
                        con_ex.execute("INSERT INTO custom_cmd VALUES (?, ?);", (cmd, msg))
                        con.commit()
                        cmd_list.append(cmd)
                        msg = await dclient.send_message(channel, '{0}, command `{1}` made! Now just run `{2}{1}` to see the '
                                                                  'message!'.format(mention, cmd, cmd_char))
                    except sqlite3.Error as e:
                        embed=discord.Embed(title="Error", description="Error when trying to add info to database! Please notify the admins!", color=0xff0000)
                        embed.set_thumbnail(url='http://i.imgur.com/dx87cAe.png')
                        embed.add_field(name="Reason", value=e.args[1], inline=False)
                        msg = await dclient.send_message(channel, embed=embed)
                        return True, 'SQLITE', 'Error when trying to insert data: {}'.format(e.args[1]), cmd_list, msg
        else:
            msg = await dclient.send_message(channel, '{}, **USAGE:** {}custcmd <cmd> <message...>'
                                       .format(mention, cmd_char))
    else:
        msg = await dclient.send_message(channel, 'You must be an administrator, {}!'.format(mention))
    return False, None, None, cmd_list, msg
