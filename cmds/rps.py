from random import choice


# RPS command
async def ex(dclient, channel, mention, a, cmd_char):
    msg = None
    a = a.split(' ')
    if len(a) > 0:
        a = a[0].lower()
        if a in ['rock', 'paper', 'scissors']:
            r = choice(['rock', 'paper', 'scissors'])
            if a == 'rock' and r == 'rock':
                await dclient.send_message(channel, "{}, you chose `{}` while I chose `{}`...it's a tie!"
                                           .format(mention, a, r))
            elif a == 'rock' and r == 'paper':
                await dclient.send_message(channel, "{}, you chose `{}` while I chose `{}`...I win! (Paper covers rock)"
                                           .format(mention, a, r))
            elif a == 'rock' and r == 'scissors':
                await dclient.send_message(channel, "{}, you chose `{}` while I chose `{}`...you win! (Rock smashes "
                                                    "scissors)".format(mention, a, r))
            elif a == 'paper' and r == 'rock':
                await dclient.send_message(channel, "{}, you chose `{}` while I chose `{}`...you win! (Paper covers "
                                                    "rock)".format(mention, a, r))
            elif a == 'paper' and r == 'paper':
                await dclient.send_message(channel, "{}, you chose `{}` while I chose `{}`...it's a tie!"
                                           .format(mention, a, r))
            elif a == 'paper' and r == 'scissors':
                await dclient.send_message(channel, "{}, you chose `{}` while I chose `{}`...I win! (Scissors cut "
                                                    "paper)".format(mention, a, r))
            elif a == 'scissors' and r == 'rock':
                await dclient.send_message(channel, "{}, you chose `{}` while I chose `{}`...I win! (Rock smashes "
                                                    "scissors)".format(mention, a, r))
            elif a == 'scissors' and r == 'paper':
                await dclient.send_message(channel, "{}, you chose `{}` while I chose `{}`...you win! (Scissors cut "
                                                    "paper)".format(mention, a, r))
            elif a == 'scissors' and r == 'scissors':
                await dclient.send_message(channel, "{}, you chose `{}` while I chose `{}`...it's a tie!"
                                           .format(mention, a, r))
        else:
            msg = await dclient.send_message(channel, '{}, you much choose between `rock`, `paper`, or `scissors`!'
                                       .format(mention))
    else:
        msg = await dclient.send_message(channel, '{}, **USAGE:** {}rps <rock|paper|scissors>'.format(mention, cmd_char))
    return msg
