# Server Info Command
async def ex(c, pch, dch, m):
    server = ''
    for svr in c.servers:
        if svr == pch.server:
            server = svr
            break
    r = '''```Markdown
# Server Information #
[ID]:       {}
[Name]:     {}
[Owner]:    {}
[Members]:  {}
[Channels]: {}
[Region]:   {}
[Roles]:    {}
[Icon]:     {}```'''.format(server.id, server.name, server.owner.nick, len(server.members), len(server.channels),
                            server.region, ', '.join(server.roles), server.icon)
    await pch.send_message(c, r)
    await dch.send_message(c, '{}, the server information has been sent in a private message.'.format(m))
