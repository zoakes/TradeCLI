import click


def greeter(**kwargs):
    out = f"{kwargs['greeting']}, {kwargs['name']}"

    if kwargs['caps']:
        out = out.upper()
    print(out)


@click.group()
def greet():
    pass


@greet.command()  # Attaches this to greet() command / function call?
@click.argument('name')
# Option with HELLo as default
@click.option('--greeting', default='Hello')
# Flag
@click.option('--caps', is_flag=True)
def hello(**kwargs):
    greeter(**kwargs)


@greet.command()
@click.argument('name')
@click.option('--greeting', default='Goodbye')
@click.option('--caps', is_flag=True)
def goodbye(**kwargs):
    greeter(**kwargs)


## ------------ Simpler way to do this stuff (https://click.palletsprojects.com/en/8.0.x/options/#boolean-flags)

# DOES NOt seem to work though?
# info() in MAIN !
# PS C:\Users\zach\PycharmProjects\CLI> python clck.py
# Hello, dickhead
# PS C:\Users\zach\PycharmProjects\CLI> python clck.py --shout
# Error: Option '--shout' requires an argument.
# PS C:\Users\zach\PycharmProjects\CLI> python clck.py --shout=True

@click.command()
@click.option('--shout', default=False)
def info(shout=False):
    output = 'Hello, dickhead'
    if shout:
        output = output.upper() + '!!!!'
    click.echo(output)


# CALL select in MAIN!
# PS C:\Users\zach\PycharmProjects\CLI> python clck.py --pnl-type=OpenPNL
# OpenPNL


@click.command()
@click.option('--pnl-type', type=click.Choice(['OpenPNL', 'ClosedPNL'], case_sensitive=False))
def select(pnl_type):
    click.echo(pnl_type)


## PURE flag ... (either pass shout, noshout, or nothing?
@click.command()
@click.argument('word')
@click.option('--shout/--no-shout', default=False)
def output(word, shout):
    if shout:
        click.echo(word.upper())
    else:
        click.echo(word)


# CALL output() in main (and ONLY output in main)
# PS C:\Users\zach\PycharmProjects\CLI> python clck.py FUCK --shout
# FUCK
# PS C:\Users\zach\PycharmProjects\CLI> python clck.py Fuck --no-shout
# Fuck

## CALL greet() in main...
# PS C:\Users\zach\PycharmProjects\CLI> python clck.py hello zach
# Hello, zach
# PS C:\Users\zach\PycharmProjects\CLI> python clck.py goodbye zach

import sys

if __name__ == '__main__':
    # greet()
    # info()

    # select()
    output()

    ## HOW to use multiple functions...
    # https://stackoverflow.com/questions/34643620/how-can-i-split-my-click-commands-each-with-a-set-of-sub-commands-into-multipl
    # https: // click.palletsprojects.com / en / 8.0.x / commands /
