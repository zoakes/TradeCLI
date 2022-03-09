import click
import fire  # Undecided on which lib to use yet...

import datetime
import rich
from rich.console import Console
from rich.prompt import Prompt
from rich.prompt import Confirm
from rich.theme import Theme
from rich import print as rprint

from rich.columns import Columns
from rich.panel import Panel

#OLD, DUMB way of doing password (REALLY, we dont need another fucking password!)
# from cfg import PASSWORD

# More current version of config (to pass a path in)
from Services.cfgParse import parse_config_file, CONFIG_PATH
# CONFIG_PATH = None

from Services.SQL import persist_globals, sql_envs, test_globals, sql_credential_test, sql_conn_test
from Services.FormatSql import UnfilledTable, UnsentTable, PendingTable, FilledTable, AllOrdersTable
from Services.globals import set_sql_ip, set_sql_user, set_sql_password, check_globals, Global

import os
import sys






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
menu = {"Main": "M",
        "Balance": "B",
        "Positions": "P",
        "P/L": "PL",
        "Orders": "O",
        "Trades": "T",
        "Log": 'L',
        'Uptime': 'U',
    }


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

    console.print(" ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~  Main Menu  ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ \n", justify='left')
    #console.print(Panel("Main Menu"))
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
        console.log('Balance: [success]$1,234,567.89')

    elif CMD == 'P':
        console.log('Positions (Table or Cards)')

    elif CMD == 'PL':
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

    # -------------------------- Accept a Config File Path (for sql login info) -------------------------------------- #

    # # To accept a CONFIG path for settings...
    path = None
    if len(sys.argv) > 1:
        path = sys.argv[1]

    # IF received path argument, persist the path to GLOBAL (global of cfgParse)
    if path:
        PASSWORD = parse_config_file(path, 'PASSWORD')
        CONFIG_PATH = path #SAVES to cfgParse GLOBAL (for use later, in OTHER parse commands)
    else:
        PASSWORD = parse_config_file(value='PASSWORD')



    # Parse SQL Envs
    a,b,c = sql_envs()

    # Unsure why these globals.globals arent working? That def cleans up the program... (IF it works)
    # prompt_for_login = check_globals() #This isn't saving to globals for some reason? (Meaning sql_envs isnt saving to globals.global variables.
    # print(prompt_for_login, a, b, c)

    prompt_for_login = test_globals()
    print(prompt_for_login, a,b,c)

    # ------------------------------ Accept user input for credentials  ---------------------------------------- #


    # username = Prompt.ask("[b]Please enter username: ", default="zach")
    # console.print(f"Username: [green]{username}")
    #
    # # Maybe this is unneeded too ? Why login, if passing credentials for MSQL connection? ------- MAKE this the SQL Password? (And pass to sql)
    # password = None
    # while password != PASSWORD:
    #     password = Prompt.ask("[b]Please enter password: ", password=True)
    #     if password == PASSWORD:
    #         console.print("[success]Successful Login.")
    #     else:
    #         console.print("[failure]Incorrect password, Please try again.")


    #TODO -- Simply READ IN (Prompt) the password / username for SQL ? -- think this is cleaner logic than passing paths to configs.   TRY both in BRANCHES, merge better option to origin?
    # MAKE this the only login,
    # TRY config (if successfully parses config, and HAS globals set, NO prompts)
    # IF still not set, prompt below for password (and do a try / except in a while loop to test the credentials)

    if not (a and b and c):
        while True:
            sql_un = Prompt.ask("[b]Please enter SQL Username (optional if config used) >>")
            if sql_un != '' and sql_un != None:
                persist_globals(un = sql_un)
                set_sql_user(sql_un)

            sql_pass = Prompt.ask("[b]Please enter SQL Password (optional if config used) >>")
            if sql_pass != '':
                persist_globals(pw=sql_pass)
                set_sql_password(sql_pass)


            if sql_credential_test():
                break
            else:
                console.print('[failure] Please Retry Entering SQL Credentials.')

    Global.StartTime = datetime.datetime.now()

    # Threading Version (Start background task -- say checking PNL or updating table, whatever). https://www.programiz.com/python-programming/time/sleep
    # t1 = threading.Thread(target=test_non_blocking, daemon=True)
    # t1.start()

    log_out = False
    cmd = main_menu()  # Update to have prompt OUTSIDE main menu? (And remove from M cmd... pass there)
    while True:
        Global.LastTime = datetime.datetime.now() #Update for uptime calcs

        sql_conn_test(True)

        cmd = Prompt.ask(">>",
                         choices=['b', 'm', 'p', 'pl', 'o', 't', 'l', 'B', 'M', 'P', 'O', 'PL', 'T', 'L', 'q', 'Q', 'U','u'],
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

        elif CMD == 'U':
            # s = f"[b]{sym}\n[blue]{str(q)}"
            # p = Panel(s, expand=True)
            uptime = Global.LastTime - Global.StartTime
            # days = uptime.days
            # hours, remainder = divmod(uptime.seconds, 3600)
            # hours = hours - (days // 1)
            # minutes, seconds = divmod(remainder, 60)

            s = f"Live since {Global.StartTime.strftime('%x')} {Global.StartTime.strftime('%X')}\nUptime: [blue]   {uptime}" ##{days}d {hours}:{minutes}:{seconds}"
            console.print(Panel(s, expand=True))

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
