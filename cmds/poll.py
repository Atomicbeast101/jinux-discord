# Poll command
async def ex_poll(dclient, channel, author, mention, a, poll, poll_question, options, votes, voted, cmd_char):
    if channel.permissions_for(author):
        a = a.split(' ')
        if len(a) >= 1:
            if a[0].lower() == 'start':
                if len(a) >= 3:
                    if poll:
                        await dclient.send_message(channel, '{}, poll is already running! If you want to close the '
                                                            'poll, do {}poll stop!'.format(mention, cmd_char))
                    else:
                        poll = True
                        i = 2
                        while i < len(a):
                            poll_question += a[i] + ' '
                            i += 1
                        options = a[1].lower().split('|')
                        votes = [0] * len(options)
                        voted = []
                        await dclient.send_message(channel, '''```CSS
[Poll Started]: {}
Answer: -vote <{}>```'''.format(poll_question, '|'.join(options)))
                else:
                    await dclient.send_message(channel, '{}, **USAGE:** {}poll start <options1|options2|etc...> '
                                                        '<question>'.format(mention, cmd_char))
            elif a[0].lower() == 'stop':
                if poll:
                    r = '''```CSS
[Poll Closed]: ''' + poll_question + '''
Results:
'''
                    cnt = 0
                    for op in options:
                        r += '''  ''' + op + ''': ''' + str(votes[cnt]) + '''
'''
                        cnt += 1
                    r += '''```'''
                    await dclient.send_message(channel, r)
                    poll = False
                    poll_question = ''
                    options = []
                    votes = []
                    voted = []
                else:
                    await dclient.send_message(channel, '{}, there is no poll running!'.format(mention))
            else:
                await dclient.send_message(channel, '{}, **USAGE:** {}poll <start|stop> <options1|options2|etc...> '
                                                    '<question>'.format(mention, cmd_char))
        else:
            await dclient.send_message(channel, '{}, **USAGE:** {}poll <start|stop> <options1|options2|etc...> '
                                                '<question>'.format(mention, cmd_char))
    else:
        await dclient.send_message(channel, 'You must be an administrator, {}!'.format(mention))
    return poll, poll_question, options, votes, voted


# Vote command
async def ex_vote(dclient, channel, au, mention, a, poll, poll_question, options, votes, voted):
    if poll:
        if au.id in voted:
            await dclient.send_message(channel, 'Are you trying to make a voting fraud, {}?'.format(mention))
        else:
            a = a.split(' ')
            if len(a) == 1 and a[0].lower() in options:
                cnt = 0
                for op in options:
                    if a[0].lower() == op:
                        votes[cnt] += 1
                        voted.append(au.id)
                        break
                    else:
                        cnt += 1
                r = '''```CSS
[Question]: ''' + poll_question + '''
'''
                cnt = 0
                for op in options:
                    r += '''  ''' + op + ''': ''' + str(votes[cnt]) + '''
'''
                    cnt += 1
                r += '''```'''
                await dclient.send_message(channel, r)
            else:
                await dclient.send_message(channel, '''{}, you must choose an option! List of available options:
```CSS
{}```'''.format(mention, ', '.join(options)))
    else:
        await dclient.send_message(channel, 'What are you trying to vote for, {}?'.format(mention))
    return poll, poll_question, options, votes, voted
