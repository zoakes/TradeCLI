from rich import print as rprint

nums_list = [1, 2, 3, 4]
rprint(nums_list)

nums_tuple = (1, 2, 3, 4)
rprint(nums_tuple)

nums_dict = {'nums_list': nums_list, 'nums_tuple': nums_tuple}
rprint(nums_dict)

bool_list = [True, False]
rprint(bool_list)

from rich.console import Console

console = Console()

console.print('test', style='white on blue')

from rich.color import Color

color = Color.parse('red')

#  ----------------------- STYLES -------------------- #
from rich.style import Style

danger_style = Style(color="red", blink=True, bold=True)

console.print("Danger, Will Robinsnon", style=danger_style)
console.log("Testing Logging (danger style)", style=danger_style)

# ----------- My Own Colors -------------- ##

cust_orange = "#FFA500"
console.log(f"[{cust_orange}]Testing use of hex colors (inline) --- cant find way to save them...")
console.log("[#FFC0CB]Pink Example...")



# ---------------- Table (From Dict) ------------------ #

def merge_dict(dict_one, dict_two):
    merged_dict = dict_one.update(dict_two)
    console.log(merged_dict, log_locals=True)


merge_dict({'id': 1}, {'name': 'Ashutosh'})

# ------------- Progress Bar -------------- #

from rich.progress import track
from time import sleep


def process_data():
    sleep(0.02)


for _ in track(range(10), description='[green]Processing data'):
    process_data()

# ------------------ Rich Columns ---------------- #
import json
from urllib.request import urlopen

from rich.console import Console
from rich.columns import Columns
from rich.panel import Panel


def get_content(user):
    """Extract text from user dict."""
    country = user["location"]["country"]
    name = f"{user['name']['first']} {user['name']['last']}"
    return f"[b]{name}[/b]\n[yellow]{country}"


console = Console()

users = json.loads(urlopen("https://randomuser.me/api/?results=30").read())["results"]
user_renderables = [Panel(get_content(user), expand=True) for user in users]
console.print(Columns(user_renderables))

# Use Markdown! for styling...
p = Panel("[b]Test String[/b]\nTest substring", expand=True)
four_ps = [p for p in range(4)]
console.print(p)
console.print(Columns([p for i in range(5)]))  # Print 5 of them...



# ------------------------ Table ! ----------------------- #

from rich.table import Table
from rich.console import Console

table = Table(title='ToDo')

table.add_column("S. No.", style="cyan", no_wrap=True)
table.add_column("Task", style="magenta")
table.add_column("Status", justify="right", style="green")

table.add_row("1", "Buy Milk", "✅")
table.add_row("2", "Buy Bread", "✅")
table.add_row("3", "Buy Jam", "❌")

console = Console()
console.print(table)


# My own table...

table = Table(title='Pending Orders')

row1 = ["1","ESHH2","1","1","0","0"]
row2 = ["2","ESH2","-1","1","0","0"]
row3 = ["3","NQH2","1","1","0","0"]
row4 = ["4","NQH2","-1","1","0","0"]

rows = [row1,row2,row3,row4]

# ---------------- ADD each column (and its respective STYLE)
table.add_column("UID",style="white", no_wrap=True)
table.add_column("Symbol", style="cyan")
table.add_column("Side", justify="right")
table.add_column("Qty", style="purple", justify="right")
table.add_column("Sent", style="yellow", justify="right")
table.add_column("Filled", style="red", justify="right")

# https://stackoverflow.com/questions/65216850/list-of-lists-into-a-python-rich-table
# for row in zip(*rows):
#     table.add_row(*row)

table.add_row(*row1)
table.add_row(*row2)
table.add_row(*row3)
table.add_row(*row4)
table.add_row(*("5","NQH2","1","1","0","0"))

console.print(table)


# ------------------ Print Config Out (Cards) ---------------------- #

root_to_qty = {"ESH2":1,"NQH2":1, "CLG2":1, "GCG2":1,"ZSK2":1}
lst = list(root_to_qty.items())
# rprint(lst)
# rprint(root_to_qty)

# Convert ot strings...
lst_of_panels = []
for sym,  q in root_to_qty.items():
    s = f"[b]{sym}\n[blue]{str(q)}"
    p = Panel(s, expand=True)
    lst_of_panels.append(p)

console.print("Configuration Cards",justify='center')
#p = Panel("[b]Test String[/b]\nTest substring", expand=True)
console.print(Columns(lst_of_panels), justify='center')

print('\n\n')

from rich.theme import Theme
custom_theme = Theme({
    "info": "dim cyan",
    #"warning": Color.parse("#F47983"), #"magenta",
    "warning":"yellow",
    "danger": "bold red"
})

console = Console(theme=custom_theme)
console.log("[#32CD32]Testing Output Styles --- (clean up later)")
console.print("This is information", style="info")
console.print("[warning]This is warning[/warning]")
console.print("This is danger",style="danger")
