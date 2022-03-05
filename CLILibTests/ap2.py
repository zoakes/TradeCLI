import argparse


def greet(args):
    out = f"{args.greeting},  {args.name}"
    if args.caps:
        out = out.upper()
    print(out)


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

hello = subparsers.add_parser('hello')
hello.add_argument("name")

# Option with DEFAULT
hello.add_argument("--greeting", default="Hello")

# Add a flag (Default = false!)
hello.add_argument("--caps", action="store_true")  # action setting means stores it as a boolean.
hello.set_defaults(func=greet)

## CTRL + ALT + SHIFT + L Reformats.

goodbye = subparsers.add_parser('goodbye')
goodbye.add_argument('name')
goodbye.add_argument('--greeting', default='Goodbye')
goodbye.add_argument('--caps',action='store_true')
goodbye.set_defaults(func=greet)


if __name__ == '__main__':
    args = parser.parse_args()

    try:
        func = args.func
    except AttributeError:
        parser.error('Too few arguments.')
    func(args)

