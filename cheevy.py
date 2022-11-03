#!/usr/bin/env python3

"""cheevy.py
by Tom Van Manen, released under Hippocratic License 2.1.

A quick CLI tool for grabbing achievements from TNNT (The November Nethack Tournament).
"""

import requests
import re
from bs4 import BeautifulSoup
import argparse

# argparse
parser = argparse.ArgumentParser(
    description="Scrape TNNT achievements from hardfought."
)
done_group = parser.add_mutually_exclusive_group()
done_group.add_argument(
    "-a",
    "--all",
    default=True,
    help="Show all achievements. (default)",
    action="store_true",
    dest="all"
)
done_group.add_argument(
    "-d",
    "--done",
    default=False,
    help="Show completed achievements.",
    action="store_true",
    dest="done"
)
done_group.add_argument(
    "-u",
    "--undone",
    default=False,
    help="Show incomplete achievements.",
    action="store_true",
    dest="undone"
)
parser.add_argument(
    "-s",
    "--search",
    metavar="STR",
    type=str,
    default="",
    help="Search achievements for a string. (case-insensitive)",
)
parser.add_argument(
    "-n",
    "--name",
    metavar="NAME",
    type=str,
    default="",
    help="Specify your hardfought.org username. Cheevy remembers the last username entered, so you only need to do this once.",
)
parser.add_argument(
    "-c",
    "--clan",
    default=False,
    help="Check your clan's achievements. (Cheevy only reports your personal achievements by default.)",
    action="store_true",
)
parser.add_argument(
    "-i",
    "--include",
    default=False,
    help="Include current game results. In order to use this option, you must first manually paste the results of the in-game #achievements command into `dump.txt`, and update as needed. (Automating this would be botting.) Please be gentle with this baby feature.",
    action="store_true",
)
args = parser.parse_args()

# get username
def get_name(f):
    if not args.name:
        name_ = f.read().strip()
        while name_ == "":
            name_ = input("Please enter your hardfought.org username: ").strip()
        args.name = name_
    f.seek(0)
    f.truncate()
    f.write(args.name)
def open_(filename, fun):
    try:
        with open(filename, "x+") as file:
           fun(file)
    except FileExistsError:
        with open(filename, "r+") as file:
           fun(file)
open_("name", get_name)

# read from user page
r = requests.get("https://tnnt.org/player/" + args.name)
if r.status_code == 404:
    print(f"Sorry, user {args.name} not found (404).")
    # print("Try \"./cheevy.py -n NAME\" to reset username."))
    print("(Check your spelling - caps matter!)")
    with open("name", "w") as file:
        pass
    exit()
soup = BeautifulSoup(r.text, 'html.parser')

# read from clan page
if args.clan:
    # def has_clan(href):
    #     return href and re.compile("clan\/[0-9]+\.html").search(href)

    try:
        # grab the clan page from player source
        clan = soup.find(href=re.compile('\/clan\/'))["href"]
        # process it
        r = requests.get("https://tnnt.org" + clan)
        soup = BeautifulSoup(r.text, 'html.parser')
    except TypeError:
        print(args.name + " doesn't have a clan.")
        raise SystemExit


# achievements = soup.find_all(class_ = "achieve-item")

# get table id="achievements-table" > tbody > tr
achievements = soup.find("table", id="achievements-table").find("tbody").find_all("tr")

# process dump.txt
dump = ""
current = {}
if args.include:
    try:
        with open("dump.txt", 'r') as f:
            dump = f.read().split('\n')
    except FileNotFoundError:
        with open("dump.txt", 'x') as f:
            pass
        print("To use --include, first paste #achievements command results into `dump.txt`.")
        input("Press ENTER to continue.")

    for line in dump:
        # for example,
        # │[X] #V11 "Anti-Stoner" - etc.
        m = re.search('\[(.)\] #... \"(.+)\" - ', line)
        if m:
            title = m.group(2).lower()
            current[title] = True if m.group(1) == 'X' else False

# For the following three achievements, name differs between
# website text      &      in-game #achievements text:
#
# Feel the Burn            We Need To Go Deeper
# Bell, Book and Candle    Bell, Book, and Candle
# Boulder Pusher           Boulder-Pusher
#
# Here, we change label to the in-game text
def cross_check(label):
    if label == "Feel the Burn":
        label = "We Need To Go Deeper"
    elif label == "Bell, Book and Candle":
        label = "Bell, Book, and Candle"
    elif label == "Boulder Pusher":
        label = "Boulder-Pusher"
    return (label.lower() in current) and current[label.lower()]

# print 'em
for tag in achievements:
    # string = tag.string.strip()
    innards = tag.text.strip().split('\n')
    string = innards[2]

    # old get status
    # if tag['class'].__contains__("achieved") or (args.include and cross_check(string)):

#    if string == "Kill it Twice":
#        print(innards)
#        break



    # new get status
    #
    # 2022: "❖" gets used for cheevos in current game
    if innards[0] == "❖" or (args.include and cross_check(string)):
        is_achieved = 2
    elif innards[0] == "✔":
        is_achieved = 1 
    else:
        is_achieved = 0

    # filter done/undone
    if args.done and not is_achieved:
        continue
    elif args.undone and is_achieved:
        continue

    # filter search
    if args.search:
        args.search = args.search.lower()
        if not ((args.search in innards[3].lower()) or (args.search in string.lower())):
        # old
        # if not ((args.search in tag['title'].lower()) or (args.search in string.lower())):
            continue




    # Spelling Test:
    # to use this, make sure dump.txt contains every cheevo :)
    #
    # if string.lower() not in current:
    #     print(string)
    #     # print(string + "    " + list(current.keys())[achievements.index(tag)])
    # continue




    # set 37 char limit
    if len(string) > 37:
        string_fit = string[:34] + "..."
    else:
        string_fit = string
    space = " " * (41 - len(string_fit))
    if is_achieved == 1:
        # checkmark
        status = "\033[92m{}\033[00m " .format(u"\u2713")
    elif is_achieved == 2:
        # current
        status = "\033[93m{}\033[00m " .format(u"\u2756")
    else:
        # cross-out
        status = "\033[91m{}\033[00m " .format("x")
    # print(status + string_fit + space + tag['title'])
    print(status + string_fit + space + innards[-1])


