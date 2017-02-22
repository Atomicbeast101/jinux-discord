# Channel Info Command
async def ex(c, pch, dch, m):
    channel = dch
    r = '''```Markdown
# Channel Information #
[ID]:             {}
[Name]:           {}
[Private]:        {}
[Position]:       {}
[Default]:        {}
[Allow Mentions]: {}
[Created]:        {}```'''.format(channel.id, channel.name, str(channel.is_private), str(channel.position),
                                  str(channel.is_default), channel.mention, channel.created_at)
    await pch.send_message(c, r)
    await dch.send_message(c, '{}, the channel information has been sent in a private message.'.format(m))
