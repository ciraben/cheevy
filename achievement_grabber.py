#!/usr/bin/env python3

"""achievement_grabber.py
by Tom Van Manen, released under Hippocratic License 2.1.

A quick CLI tool for grabbing achievements from TNNT (The November Nethack Tournament).
"""

import requests
import re
from bs4 import BeautifulSoup
import argparse

# argparse
parser = argparse.ArgumentParser(
    description="Scrape TNNT clan achievements from hardfought."
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
    help="Specify your hardfought.org username. Achievement-grabber remembers the last username entered, so you only need to do this once.",
)
parser.add_argument(
    "-c",
    "--clan",
    default=False,
    help="Check your clan's achievements. (Achievement-grabber only reports your personal achievements by default.)",
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
try:
    with open("name", "x+") as file:
       get_name(file)
except FileExistsError:
    with open("name", "r+") as file:
       get_name(file)

# read from user page
r = requests.get("https://www.hardfought.org/tnnt/players/" + args.name + ".html")
if r.status_code == 404:
    print(f"Sorry, user {args.name} not found (404).")
    # print("Try \"./achievement_grabber.py -n NAME\" to reset username."))
    print("(Check your spelling - caps matter!)")
    with open("name", "w") as file:
        pass
    exit()
soup = BeautifulSoup(r.text, 'html.parser')

# read from clan page
if args.clan:
    def has_clan(href):
        return href and re.compile("clans\/[0-9]+\.html").search(href)
    clan = soup.find(href=has_clan)["href"]
    r = requests.get("https://www.hardfought.org/tnnt/" + clan)
    soup = BeautifulSoup(r.text, 'html.parser')

if args.done:
    achievements = soup.find_all(class_ = "achieved")
elif args.undone:
    achievements = soup.find_all(class_ = "not-achieved")
else:
    achievements = soup.find_all(class_ = "achieve-item")

for tag in achievements:
    string = tag.string.strip()

    # filter search
    if args.search:
        args.search = args.search.lower()
        if ((args.search in tag['title'].lower()) or (args.search in string.lower())):
            pass
        else:
            continue

    # set 37 char limit
    if len(string) > 37:
        string = string[:34] + "..."
    space = " " * (41 - len(string))
    if tag['class'].__contains__("achieved"):
        status = "\033[92m{}\033[00m " .format(u"\u2713")
    else:
      status = "\033[91m{}\033[00m " .format("x")
    print(status + string + space + tag['title'])
