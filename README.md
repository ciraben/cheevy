# achievement_grabber.py
#### by Tom Van Manen, released under Hippocratic License 2.1.

A quick CLI tool for grabbing achievements from [TNNT](https://www.hardfought.org/tnnt/) (The November Nethack Tournament).

## Installation

Get `achievement-grabber.py` with

```bash
$ git clone "https://github.com/ciraben/achievement-grabber"
```

Make the script executable with

```bash
$ chmod +x /path/to/achievement-grabber.py
```

[Get Python 3](https://www.python.org/downloads/).

Install Python 3 dependencies with PyPi:

```bash
$ pip3 install requests BeautifulSoup4
```

Run `achievement_grabber.py` with any of

```bash
$ python3 /path/to/achievement_grabber.py
$ /path/to/achievement_grabber.py
$ ./achievement_grabber.py   # if current directory
```

The first time you run it, `achievement_grabber.py` will prompt you for a [hardfought.org](https://hardfought.org) username to inspect. Ensure proper capitalization. You can edit this at any time with the `-n NAME` argument.

By default, only user achievements are reported. For clan achievements, run with `-c` or `--clan` argument.

See `./achievement_grabber.py --help` for more options.

## Including Current Game Achievements

To include current game results in `achievement-grabber.py` output, you must first manually paste the results of the in-game `#achievements` command into `dump.txt`, and update as needed. (Automating this would be botting, which is against tournament rules.)

This means logging into your current game, typing in the `#achievements` extended command, and choosing option `e` (or `b`).
Then paste the text output from your screen into `dump.txt`. Repeat for each page - order doesn't matter.
It's fine to paste surrounding text too, or the whole window, no worries about that.
See `sample-dump.txt` if you're unsure. Works with curses or tty.

I know this seems like a cumbersome "no bots" work-around, but it's actually pretty handy! Once you have your `dump.txt` in place, you can run subsequent searches for achievements you half-remember needing.

```bash
$ ./achievement-grabber.py --include --search tree
✓ Isaac Newton                             Get fruit by kicking a tree
$ ./achievement-grabber.py -is bullwhip
x Indiana Jones                            Disarm a monster with a bullwhip
```

You can get a full night's sleep before your ascension run, without having to recall whether you nabbed that Oracle achievement on the way down.

```bash
$ ./achievement-grabber.py -is oracle
x Sage Advice                              Consult the Oracle
```

And you can easily check whether those extra wands are worth something before dumping them.

```bash
$ ./achievement-grabber.py -uis wand
x That Wand is Mine                        Kill Orcus
x Predictably, Nothing Happens             Break an identified wand of nothing
x Dust to Dust                             Wrest one last charge from a wand of wishing
x The Deathly Hallows                      Wield a wand of death while wearing an invisibility cloak and amulet of life saving
x Wanton Waste                             Break an identified, charged wand of wishing
x Mikado                                   Identify all wands
```

With just a few keystrokes, `achievement-grabber.py` takes care of searching and cross-referencing achievements for you, and keeps your focus on the game.
