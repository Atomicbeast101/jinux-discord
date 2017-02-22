# Channel Info Command
async def ex(c, pch, dch, m):
    channel = dch
    r = '''```Markdown
# Channel Information #
[ID]:             {}
[Name]:           {}
[Topic]:          {}
[Private]:        {}
[Position]:       {}
[Default]:        {}
[Created]:        {}```'''.format(channel.id, channel.name, channel.topic, str(channel.is_private),
                                  str(channel.position), str(channel.is_default), channel.created_at)
    await c.send_message(pch, r)
    await c.send_message(dch, '{}, the channel information has been sent in a private message.'.format(m))
