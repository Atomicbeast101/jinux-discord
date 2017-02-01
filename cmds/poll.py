from config import CMD_CHAR


# Poll command
async def ex_poll(c, ch, au, m, a, pll, q, opt, vts, vtd):
    if ch.permissions_for(au):
        a = a.split(' ')
        if len(a) >= 2:
            if a[0].lower() == 'start':
                if len(a) >= 4:
                    if pll:
                        await c.send_message(ch, '{}, poll is already running! If you want to close the poll, do {}poll'
                                                 ' stop!'.format(m, CMD_CHAR))
                    else:
                        pll = True
                        i = 2
                        while i < len(a):
                            q += a[i] + ' '
                        opt = a[1].lower().split('|')
                        vts = []
                        vtd = []
                        await c.send_message(ch, '''```CSS
                                                    [Poll Started]: {}
                                                    Answer: -yes  OR  -no```''')
                else:
                    await c.send_message(ch, '{}, **USAGE:** {}poll start <options1|options2|etc...> <question>'.
                                         format(m, CMD_CHAR))
            elif a[0].lower() == 'stop':
                if pll:
                    pll = False
                    q = ''
                    opt = []
                    vts = []
                    vtd = []
                    r = '''```CSS
                           [Poll Closed]: ''' + q + '''
                           Results:
                           '''
                    cnt = 0
                    for op in opt:
                        r += '''  ''' + op + ''': ''' + vts[cnt] + '''
                                '''
                        cnt += 1
                    await c.send_message(ch, r)
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
    return pll, q, opt, vts, vtd


# Vote command
async def ex_vote(c, ch, au, m, a, pll, q, opt, vts, vtd):
    if pll:
        if au.id in vtd:
            await c.send_message(ch, 'What are you trying to make a voting fraud, {}?'.format(m))
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
                       [Question]: ''' + q + '''
                       '''
                cnt = 0
                for op in opt:
                    r += '''  ''' + op + ''': ''' + vts[cnt] + '''
                            '''
                    cnt += 1
                await c.send_message(ch, r)
            else:
                await c.send_message(ch, '''{}, you must choose an option! List of available options:
                                            ```CSS
                                            {}```'''.format(m, ', '.join(opt)))
    else:
        await c.send_message(ch, 'What are you trying to vote for, {}?'.format(m))
    return pll, q, opt, vts, vtd
