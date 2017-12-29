import discord


def usage_msg(_cmd, _mention, _cmdchar):
    return ':warning: {} **USAGE:** {}{}'.format(_mention, _cmdchar, _cmd)


def create_embed(status, question, options, votes):
    if status == 'OPEN':
        embed = discord.Embed(title='{}: -vote <{}>'.format(status, '|'.join(options)),  color=0x00ff00)
        embed.set_author(name=question, icon_url='https://i.imgur.com/vxdjxn3.jpg')
        step = 0
        for option in options:
            embed.add_field(name=option, value=str(votes[step]), inline=True)
            step += 1
        return embed
    else:
        embed = discord.Embed(title='{}: -vote <{}>'.format(status, '|'.join(options)), color=0xff0000)
        embed.set_author(name=question, icon_url='https://i.imgur.com/vxdjxn3.jpg')
        step = 0
        for option in options:
            embed.add_field(name=option, value=str(votes[step]), inline=True)
            step += 1
        return embed


class Poll:
    def __init__(self):
        self.active = False
        self.question = ''
        self.options = []
        self.votes = []
        self.voted = []

    async def poll(self, _dclient, _channel, _mention, _cmdchar, _msg):
        _msg = _msg.split(' ')
        if len(_msg) >= 2:
            _msg.pop(0)
            if _msg[0].lower() == 'start':
                if len(_msg) >= 3:
                    if '|' in _msg[1]:
                        if self.active:
                            await _dclient.send_message(_channel, ':warning: {} There is already a poll running!'
                                                        .format(_mention))
                        else:
                            self.active = True
                            for i in range(2, len(_msg)):
                                self.question += _msg[i] + ' '
                            self.options = _msg[1].lower().split('|')
                            self.votes = [0] * len(self.options)
                            self.voted = []
                            await _dclient.send_message(_channel, embed=create_embed('OPEN', self.question,
                                                                                     self.options, self.votes))
                    else:
                        await _dclient.send_message(_channel, ':warning: {} Can\'t be a poll if there\'s only one '
                                                              'option! Please separate each option by `|`! Example: '
                                                              '`{}vote <yes|no>` Do you like hotdogs?'
                                                    .format(_mention, _cmdchar))
                else:
                    await _dclient.send_message(_channel, usage_msg('poll start <options by |> <question...>',
                                                                    _mention, _cmdchar))
            elif _msg[0].lower() == 'status':
                if self.active:
                    await _dclient.send_message(_channel, embed=create_embed('OPEN', self.question,
                                                                             self.options, self.votes))
                else:
                    await _dclient.send_message(_channel, ':warning: {} There is no poll running!'.format(_mention))
            elif _msg[0].lower() == 'stop':
                if self.active:
                    await _dclient.send_message(_channel, embed=create_embed('CLOSED', self.question,
                                                                             self.options, self.votes))
                    self.active = False
                    self.question = ''
                    self.options = []
                    self.votes = []
                    self.voted = []
                else:
                    await _dclient.send_message(_channel, ':warning: {} There is no poll to stop!'.format(_mention))
            else:
                await _dclient.send_message(_channel, usage_msg('poll <start|stop> <options by |> <question...>',
                                                                _mention, _cmdchar))
        else:
            await _dclient.send_message(_channel, usage_msg('poll <start|stop> <options by |> <question...>', _mention,
                                                            _cmdchar))

    async def vote(self, _dclient, _channel, _mention, _cmdchar, _msg, _author):
        if self.active:
            if _author.id in self.voted:
                await _dclient.send_message(_channel, ':warning: {} Are you trying to commit a voting fraud, human?'
                                            .format(_mention))
            else:
                _msg = _msg.split(' ')
                if len(_msg) == 2 and _msg[1].lower() in self.options:
                    spot = 0
                    for option in self.options:
                        if _msg[1].lower() == option:
                            self.votes[spot] += 1
                            self.voted.append(_author.id)
                            break
                        spot += 1
                    await _dclient.send_message(_channel, embed=create_embed('OPEN', self.question,
                                                                             self.options, self.votes))
                else:
                    await _dclient.send_message(_channel, 'vote <{}>'.format('|'.join(self.options), _mention,
                                                                             _cmdchar))
        else:
            await _dclient.send_message(_channel, ':warning: {} There is no poll to vote on!'.format(_mention))
