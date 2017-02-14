# Poll command
async def ex_poll(c, ch, au, m, a, poll, poll_question, opt, vts, vtd, CMD_CHAR):
    if ch.permissions_for(au):
        a = a.split(' ')
        if len(a) >= 1:
            if a[0].lower() == 'start':
                if len(a) >= 3:
                    if poll:
                        await c.send_message(ch, '{}, poll is already running! If you want to close the poll, do {}poll'
                                                 ' stop!'.format(m, CMD_CHAR))
                    else:
                        poll = True
                        i = 2
                        while i < len(a):
                            poll_question += a[i] + ' '
                            i += 1
                        opt = a[1].lower().split('|')
                        vts = [0] * len(opt)
                        vtd = []
                        await c.send_message(ch, '''```CSS
[Poll Started]: {}
Answer: -vote <{}>```'''.format(poll_question, '|'.join(opt)))
                else:
                    await c.send_message(ch, '{}, **USAGE:** {}poll start <options1|options2|etc...> <question>'.
                                         format(m, CMD_CHAR))
            elif a[0].lower() == 'stop':
                if poll:
                    r = '''```CSS
[Poll Closed]: ''' + poll_question + '''
Results:
'''
                    cnt = 0
                    for op in opt:
                        r += '''  ''' + op + ''': ''' + str(vts[cnt]) + '''
'''
                        cnt += 1
                    r += '''```'''
                    await c.send_message(ch, r)
                    poll = False
                    poll_question = ''
                    opt = []
                    vts = []
                    vtd = []
                else:
                    await c.send_message(ch, '{}, there is no poll running!'.format(m))
            else:
                await c.send_message(ch, '{}, **USAGE:** {}poll <start|stop> <options1|options2|etc...> <question'
                                         '>'.format(m, CMD_CHAR))
        else:
            await c.send_message(ch, '{}, **USAGE:** {}poll <start|stop> <options1|options2|etc...> <question'
                                     '>'.format(m, CMD_CHAR))
    else:
        await c.send_message(ch, 'You must be an administrator, {}!'.format(m))
    return poll, poll_question, opt, vts, vtd


# Vote command
async def ex_vote(c, ch, au, m, a, poll, poll_question, opt, vts, vtd):
    if poll:
        if au.id in vtd:
            await c.send_message(ch, 'Are you trying to make a voting fraud, {}?'.format(m))
        else:
            a = a.split(' ')
            if len(a) == 1 and a[0].lower() in opt:
                cnt = 0
                for op in opt:
                    if a[0].lower() == op:
                        vts[cnt] += 1
                        vtd.append(au.id)
                        break
                    else:
                        cnt += 1
                r = '''```CSS
[Question]: ''' + poll_question + '''
'''
                cnt = 0
                for op in opt:
                    r += '''  ''' + op + ''': ''' + str(vts[cnt]) + '''
'''
                    cnt += 1
                r += '''```'''
                await c.send_message(ch, r)
            else:
                await c.send_message(ch, '''{}, you must choose an option! List of available options:
```CSS
{}```'''.format(m, ', '.join(opt)))
    else:
        await c.send_message(ch, 'What are you trying to vote for, {}?'.format(m))
    return poll, poll_question, opt, vts, vtd
