

from Services.SQL import *
from rich.table import Table
from rich.console import Console


def CreateOrdersTable(sql_callback, title):

    res = sql_callback()
    #print(res)

    table = Table(title=title)
    table.add_column("UID", style="white", no_wrap=True)
    table.add_column("Symbol", style="cyan")
    table.add_column("Side", justify="right")
    table.add_column("Qty", style="purple", justify="right")
    table.add_column("Sent", style="yellow", justify="right")
    table.add_column("Filled", style="red", justify="right")

    for tup in res:
        #table.add_row(*tup)
        as_str = [str(i) for i in tup]
        table.add_row(*as_str)

    console = Console()
    console.print(table)

# ------------------------ Helpers ---------------------- #

def AllOrdersTable(title='All Orders'):
    CreateOrdersTable(get_all_orders, title)

def UnfilledTable(title='Active Orders'):
    CreateOrdersTable(get_all_unfilled, title)

def UnsentTable(title='Unsent Orders'):
    CreateOrdersTable(get_all_unsent, title)

def PendingTable(title='Pending Orders'):
    CreateOrdersTable(get_all_pending, title)

def FilledTable(title='Trades (filled orders)'):
    CreateOrdersTable(get_all_filled, title)

# ---------------------------------------- Test Logic ------------------------------------- #




def TestTables():
    CreateOrdersTable(get_all_unfilled, "Unfilled Orders")

    CreateOrdersTable(get_all_pending, 'Pending Orders')

    CreateOrdersTable(get_all_unsent, 'Unsent Orders')

    AllOrdersTable()
    PendingTable()
    UnsentTable()
    UnfilledTable()
    FilledTable()

if __name__ == '__main__':
    TestTables()