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
