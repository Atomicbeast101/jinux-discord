import discord
import re


def usage_msg(_cmd, _mention, _cmdchar):
    return ':warning: {} **USAGE:** {}{}'.format(_mention, _cmdchar, _cmd)


def cmd_valid(_cmd):
    if re.match('^[\w\d_-]*$', _cmd):
        return True
    return False


def get_name(_dclient, _server, _id):
    return discord.utils.get(discord.utils.get(_dclient.servers, id=_server.id).members, id=_id).name


class CustCmd:
    def __init__(self, _db, _db_ex):
        self.db = _db
        self.db_ex = _db_ex

    async def execute(self, _dclient, _channel, _mention, _cmdchar, _msg, _author, _cmd_list, _cus_cmdcharlimit):
        _msg = _msg.split(' ')
        if len(_msg) > 1:
            _msg.pop(0)
            if _msg[0].lower() == 'add':
                if len(_msg) >= 3:
                    cmd = _msg[1].lower()
                    if cmd_valid(cmd):
                        if cmd in _cmd_list:
                            await _dclient.send_message(_channel, ':warning: {} Command `{}` already exists!'
                                                        .format(_mention, cmd))
                        else:
                            if len(cmd) > 20:
                                await _dclient.send_message(_channel, ':warning: {} Command `{}` cannot be more than '
                                                                      '`20` characters long!'.format(_mention, cmd))
                            else:
                                if len(cmd) > _cus_cmdcharlimit:
                                    await _dclient.send_message(_channel, ':warning: {} Command `{}` cannot be more '
                                                                          'than `{}` characters long!'
                                                                .format(_mention, cmd, _cus_cmdcharlimit))
                                else:
                                    msg = ''
                                    for i in range(2, len(_msg)):
                                        msg += _msg[i] + ' '
                                    self.db_ex.execute('INSERT INTO custom_cmd VALUES (?, ?, ?);', (cmd, _author.id,
                                                                                                    msg))
                                    self.db.commit()
                                    await _dclient.send_message(_channel, '{} Command `{}` has been made!'
                                                                .format(_mention, cmd))
                    else:
                        await _dclient.send_message(_channel, ':warning: {} Command names can only contain '
                                                              'any `numbers`, `letters`, and `_` & `-`. '
                                                    .format(_mention))
                else:
                    await _dclient.send_message(_channel, usage_msg('custcmd add <cmd> <message...>', _mention,
                                                                    _cmdchar))
            elif _msg[0].lower() == 'set':
                if len(_msg) >= 3:
                    cmd = _msg[1].lower()
                    if cmd in _cmd_list:
                        msg = ''
                        for i in range(2, len(_msg)):
                            msg += _msg[i] + ' '
                        owner = 0
                        for row in self.db_ex.execute('SELECT owner FROM custom_cmd WHERE command=?;', (cmd, )):
                            owner = row[0]
                            break
                        if _author.id == owner:
                            self.db_ex.execute('UPDATE custom_cmd SET message=? WHERE command=?;', (msg, cmd))
                            self.db.commit()
                            await _dclient.send_message(_channel, '{} Command `{}` has been updated!'
                                                        .format(_mention, cmd))
                        elif _channel.permissions_for(_author).administrator:
                            self.db_ex.execute('UPDATE custom_cmd SET message=? WHERE command=?;', (msg, cmd))
                            self.db.commit()
                            await _dclient.send_message(_channel, '{} Command `{}` has been updated!'
                                                        .format(_mention, cmd))
                        else:
                            await _dclient.send_message(_channel, '{} You do not own this command `{}`!'
                                                        .format(_mention, cmd))
                    else:
                        await _dclient.send_message(_channel, ':warning: {} Command `{}` doesn\'t exist!'
                                                    .format(_mention, cmd))
                else:
                    await _dclient.send_message(_channel, usage_msg('custcmd set <cmd> <message...>', _mention,
                                                                    _cmdchar))
            elif _msg[0].lower() == 'remove':
                if len(_msg) == 2:
                    cmd = _msg[1].lower()
                    if cmd in _cmd_list:
                        owner = 0
                        for row in self.db_ex.execute('SELECT owner FROM custom_cmd WHERE command=?;', (cmd, )):
                            owner = row[0]
                            break
                        if _author.id == owner:
                            self.db_ex.execute('DELETE FROM custom_cmd WHERE command=?;', (cmd, ))
                            self.db.commit()
                            await _dclient.send_message(_channel,
                                                        '{} Command `{}` has been removed!'.format(_mention, cmd))
                        elif _channel.permissions_for(_author).administrator:
                            self.db_ex.execute('DELETE FROM custom_cmd WHERE command=?;', (cmd,))
                            self.db.commit()
                            await _dclient.send_message(_channel,
                                                        '{} Command `{}` has been removed!'.format(_mention, cmd))
                        else:
                            await _dclient.send_message(_channel, '{} You do not own this command `{}`!'
                                                        .format(_mention, cmd))
                    else:
                        await _dclient.send_message(_channel, ':warning: {} Command `{}` doesn\'t exist!'
                                                    .format(_mention, cmd))
                else:
                    await _dclient.send_message(_channel, usage_msg('custcmd remove <cmd>', _mention,
                                                                    _cmdchar))
            elif _msg[0].lower() == 'list':
                commands = {}
                for row in self.db_ex.execute('SELECT command, owner FROM custom_cmd;'):
                    commands[row[0]] = row[1]
                result = '''**Custom Command List:**
```Markdown
'''
                result += '''{:20} {:10}
'''.format('# Command', '# Owner')
                for key, value in commands.items():
                    result += '''{:20} {:10}
'''.format(key, get_name(_dclient, _channel.server, value))
                result += '''```'''
                await _dclient.send_message(_channel, result)
            else:
                await _dclient.send_message(_channel, usage_msg('custcmd <add|set|remove|list>',
                                                                _mention, _cmdchar))
        else:
            await _dclient.send_message(_channel, usage_msg('custcmd <add|set|remove|list>', _mention,
                                                            _cmdchar))
