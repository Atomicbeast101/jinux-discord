from bin import data

async def execute(_dclient, _channel, _mention, _cmdchar, _msg, _author):
    _msg = _msg.split(' ')
    if len(_msg) == 1:
        response = '''**Help Guide:**
```'''
        for key, value in data.help_guide.items():
            response += '''{0}{1:10} {2}
'''.format(_cmdchar, key, value)
        response += '''```'''
        await _dclient.send_message(_author, response)
        await _dclient.send_message(_channel, '{} Help guide has been sent to you directly.'.format(_mention))
    else:
        _msg.pop(0)
        if _msg[0].lower() in data.full_help_guide:
            guide = data.full_help_guide[_msg[0].lower()]
            response = '''**{} Help Guide:**
Description: `{}`
Usages:
```'''.format(_msg[0].lower().title(), guide['desc'])
            response += '''```
'''
            for key, value in guide['usage'].items():
                response += '''{:40} {}
'''.format(key, value)
            response += '''
```'''
            await _dclient.send_message(_author, response)
            await _dclient.send_message(_channel, '{} Help guide for `{}` command has been sent to you directly.'
                                        .format(_mention, _msg[0].lower()))
        else:
            await _dclient.send_message(_channel, ':warning: {} Command `{}` doesn\'t exist!'.format(_mention,
                                                                                                     _msg[0].lower()))
