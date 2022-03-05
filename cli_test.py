import click
import fire  # Undecided on which lib to use yet...

import rich
from rich.console import Console
from rich.prompt import Prompt
from rich.prompt import Confirm
from rich.theme import Theme
from rich import print as rprint

from rich.columns import Columns
from rich.panel import Panel

from cfg import PASSWORD

from Services.FormatSql import UnfilledTable, UnsentTable, PendingTable, FilledTable, AllOrdersTable

'''
#Can replicate quickfix -- call a nonblocking coro / thread that will print things (all while reading in main thread / process)
https://github.com/zoakes/FIX-OMS/blob/7e4d4eea1070e6e08bfd666cc9e6136e9c594316/initiator/application.py#L235

'''

import threading
import time
import asyncio


def test_non_blocking():
    # https://www.programiz.com/python-programming/time/sleep
    while True:
        time.sleep(5)
        console.log('Live (thread 1)')


async def test_non_block():
    while True:
        await asyncio.sleep(5)
        print('Still running (async)')


# -------------------------------- Rich Helpers ---------------------------- #
menu = {"Main": "M", "Balance": "B", "Positions": "P", "P/L": "PL", "Orders": "O", "Trades": "T", "Log": 'L'}


def main_menu():
    """
    Renders main menu (DOES NOT receive a readline -- used to)
    :return: NONE
    """
    global menu

    # Convert ot strings...
    lst_of_panels = []
    for sym, q in menu.items():
        s = f"[b]{sym}\n[blue]{str(q)}"
        p = Panel(s, expand=True)
        lst_of_panels.append(p)

    console.print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Main Menu  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ ", justify='left')
    console.print(Columns(lst_of_panels), justify='left')

    # Unsure if I want this here, or AFTER main_menu called...
    # cmd = Prompt.ask("")
    # cmd = Prompt.ask("",choices=['b','m','p','pl','o','t','l', 'B','M','P','O','PL','T','L'], show_choices=False)
    # return cmd.upper()


# Just keep it in main, no need.
def parse_main_menu(cmd):
    CMD = cmd.upper()
    if CMD == 'M':
        cmd = main_menu()  # Maybe pass on this instead?

    elif CMD == 'B':
        # TODO: Lookup balance here (in SQL !)
        console.log('Balance: [success]$1,234,567.89')

    elif CMD == 'P':
        # TODO: lookup positions
        console.log('Positions (Table or Cards)')

    elif CMD == 'PL':
        # TODO: lookup pnl
        console.log('PNL $(1,234.56)')

    elif CMD == 'O':
        console.log('Orders (Table)')

    elif CMD == 'T':
        console.log('Trades (Table)')
    elif CMD == 'L':
        console.log('Log -- make live updating thread?')

    elif CMD == 'Q':
        confirm_log_out = Confirm.ask("Do you like rich?")
        if confirm_log_out:
            return False
    else:
        pass


# --------------------------------- Rich Text Formatting --------------------------------- #

custom_theme = Theme({
    "info": "dim cyan",
    # "warning": Color.parse("#F47983"), #"magenta",
    "warning": "yellow",
    "danger": "bold red",
    "success": "green",
    "failure": "red"
})

console = Console(theme=custom_theme)

if __name__ == '__main__':
    # username = str(input("Please enter username."))

    username = Prompt.ask("[b]Please enter username: ", default="zoakes")
    console.print(f"Username: [green]{username}")

    password = None
    while password != PASSWORD:
        password = Prompt.ask("[b]Please enter password: ", password=True)
        if password == PASSWORD:
            console.print("[success]Successful Login.")
        else:
            console.print("[failure]Incorrect password, Please try again.")

    # Threading Version (Start background task -- say checking PNL or updating table, whatever). https://www.programiz.com/python-programming/time/sleep

    # t1 = threading.Thread(target=test_non_blocking, daemon=True)
    # t1.start()

    log_out = False
    cmd = main_menu()  # Update to have prompt OUTSIDE main menu? (And remove from M cmd... pass there)
    while True:

        cmd = Prompt.ask(">>",
                         choices=['b', 'm', 'p', 'pl', 'o', 't', 'l', 'B', 'M', 'P', 'O', 'PL', 'T', 'L', 'q', 'Q'],
                         show_choices=False)
        CMD = cmd.upper()

        # Main Menu
        if CMD == 'M':
            cmd = main_menu()  # Maybe pass on this instead?

        # Balance
        elif CMD == 'B':
            # TODO: Lookup balance here (in SQL !) (Same SQL Table -- save BALANCE as well)
            #  Table Structure -- IF NO SYMBOL, create TOTAL table (OR leave EMPTY line for TOTAL with others?)
            console.log('Balance: [success]$1,234,567.89')

        # Positions (Filled Orders? Or Net Position?)
        elif CMD == 'P':
            # console.log('Positions (Table or Cards)')
            FilledTable('Positions (Filled Orders) -- replace with Net Position later.')

        # Profit / Loss
        elif CMD == 'PL':
            # TODO: lookup pnl (Save another Sql Table with PNL status from rithmic?)
            #  Table Structure: Symbol, Net Position, Basis?, Open PNL, Closed PNL, Balance)
            console.log('PNL $(1,234.56)')

        # Orders (Pending)
        elif CMD == 'O':
            # console.log('Orders (Table)')
            # AllOrdersTable()
            UnsentTable()
            PendingTable()

        # Trades (Filled Orders)
        elif CMD == 'T':
            # console.log('Trades (Table)')
            FilledTable()

        elif CMD == 'L':
            # console.log('Log -- make live updating thread eventually?')
            AllOrdersTable()

        elif CMD == 'Q':
            confirm_log_out = Confirm.ask("Are you sure you want to log out?")
            if confirm_log_out:
                log_out = True
        else:
            pass

        if log_out:
            break

    console.print("[blue]Logging Out...")
    time.sleep(1)
    console.print("Goodbye.")

    # FOR prompts... will need to have a MAIN menu, and BACK as an option.
    # Would go to main menu, select whatever, then go back, etc.

    # DONT think I want this, because I dont want to print endlessly, likely want a true command line after this?
    # Otherwise, will be adding threads, etc.

    # FOR Yes / No stuff... https://rich.readthedocs.io/en/stable/prompt.html
    # is_rich_great = Confirm.ask("Do you like rich?")
    # console.print(f"Is Great? {is_rich_great}", style='green on white')
