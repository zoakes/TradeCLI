import click

'''
@click.group()
@click.version_option()
def cli():
    pass ## Entry point...


@cli.group()
@click.pass_context
def cloudfare(ctx):
    print('Cloudfare called...')

@cloudflare.group('zone')
def cloudflare_zone():
    print('cloudfare zone called...')



@cloudflare_zone.command('add')
@click.option('--jumpstart', '-j', default=True)
@click.option('--organization', '-o', default='')
@click.argument('url')
@click.pass_obj
@__cf_error_handler
def cloudflare_zone_add(ctx, url, jumpstart, organization):
    pass

'''



@click.group()
def greet():
    pass


@greet.command()  # Attaches this to greet() command / function ?
@click.argument('name') #Required...
# Option with HELLo as default
@click.option('--greeting', default='Hello')
# Flag
@click.option('--caps', is_flag=True)
def hello(**kwargs):
    print(kwargs)
    print(kwargs['caps'])
    print(kwargs['greeting'])


@greet.command()
@click.argument('name')
@click.option('--greeting', default='Goodbye')
@click.option('--caps', is_flag=True)
def goodbye(**kwargs):
    print('THIS is called when goodbye is passed! (optional CAPS is called)')
    print(kwargs['caps'])
    print(kwargs['greeting'])

## CALL greet() in main...
# PS C:\Users\zach\PycharmProjects\CLI> python clck.py hello zach
# Hello, zach
# PS C:\Users\zach\PycharmProjects\CLI> python clck.py goodbye zach

# PS C:\Users\zach\PycharmProjects\CLI> python click_advanced.py hello f --caps
# {'caps': True, 'name': 'f', 'greeting': 'Hello'}
# True
# Hello

if __name__ == '__main__':
    greet()