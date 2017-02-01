from random import choice


# RPS command
async def ex(c, ch, m, a, CMD_CHAR):
    a = a.split(' ')
    if len(a) > 0:
        a = a[0].lower()
        if a in ['rock', 'paper', 'scissors']:
            r = choice(['rock', 'paper', 'scissors'])
            if a == 'rock' and r == 'rock':
                await c.send_message(ch, "{}, you chose `{}` while I chose `{}`...it's a tie!".format(m, a, r))
            elif a == 'rock' and r == 'paper':
                await c.send_message(ch, "{}, you chose `{}` while I chose `{}`...I win! (Paper covers rock)"
                                     .format(m, a, r))
            elif a == 'rock' and r == 'scissors':
                await c.send_message(ch, "{}, you chose `{}` while I chose `{}`...you win! (Rock smashes scissors)"
                                     .format(m, a, r))
            elif a == 'paper' and r == 'rock':
                await c.send_message(ch, "{}, you chose `{}` while I chose `{}`...you win! (Paper covers rock)"
                                     .format(m, a, r))
            elif a == 'paper' and r == 'paper':
                await c.send_message(ch, "{}, you chose `{}` while I chose `{}`...it's a tie!".format(m, a, r))
            elif a == 'paper' and r == 'scissors':
                await c.send_message(ch, "{}, you chose `{}` while I chose `{}`...I win! (Scissors cut paper)"
                                     .format(m, a, r))
            elif a == 'scissors' and r == 'rock':
                await c.send_message(ch, "{}, you chose `{}` while I chose `{}`...I win! (Rock smashes scissors)"
                                     .format(m, a, r))
            elif a == 'scissors' and r == 'paper':
                await c.send_message(ch, "{}, you chose `{}` while I chose `{}`...you win! (Scissors cut paper)"
                                     .format(m, a, r))
            elif a == 'scissors' and r == 'scissors':
                await c.send_message(ch, "{}, you chose `{}` while I chose `{}`...it's a tie!".format(m, a, r))
        else:
            await c.send_message(ch, '{}, you much choose between `rock`, `paper`, or `scissors`!'.format(m))
    else:
        await c.send_message(ch, '{}, **USAGE:** {}rps <rock|paper|scissors>'.format(m, CMD_CHAR))
