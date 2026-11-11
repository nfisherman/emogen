#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
cli.py

CLI interface for emogen.py.
"""

__program__ = 'emogen'
__author__ = 'nfisherman'
__copyright__ = 'Copyright (c) 2026 nfisherman'
__credits__ = 'See "References" in /README.md'
__license__ = '0BSD'
__version__ = '1.0.0'
__status__ = "Production"

import argparse, emogen, os, sys
from pathlib import Path
from typing import Final
from random import randrange, choice

if __name__ != '__main__':
    sys.exit(1)

class __EmogenCLI(emogen.Emogen):
    """
    A child of Emogen which has hooks for verbose output.
    """

    def __init__(self,
            verbose: bool,
            dumb_terminal: bool,
            data_source: Path,
            endcaps_chance: int,
            l33t_chance: int,
            seperator_chance: int):
        """
        Same as super().__init__() but every argument is required and 
        includes an argument for verbose output.

        Args:
            verbose (bool): whether or not to log text transformations
            dumb_terminal (bool): whether or not we can use fancy
                                    formatting :D
        """

        self.verbose: bool = verbose
        self.dumb_terminal: bool = dumb_terminal
        super().__init__(
            data_source,
            self.int_in_bounds(endcaps_chance),
            self.int_in_bounds(l33t_chance),
            self.int_in_bounds(seperator_chance)
        )

    def int_in_bounds(self, number: int) -> int:
        """
        Helper function that ensures argument is within the range of 0-100.

        Args:
            number (int): the number to check

        Returns:
            int: the inputted integer in range 0-100
        """
        if number > 100:
            return 100
        if number < 0:
            return 0
        return number

    def generate(self) -> str:
        """
        Same as super().generate() but with hooks for verbose
        output.
        """

        chosen: list[str] = self.choose_name()
        if self.verbose:
            print(f'Chose: {"|".join(chosen)}')

        applied_endcaps: list[str] = super().apply_endcaps(chosen)
        print_endcaps: str = None
        if self.verbose:
            print_endcaps = "|".join([i for i in applied_endcaps if i != ''])
            if self.endcaps_chance != 0 and [applied_endcaps[0], applied_endcaps[-1]] != ['', '']:
                print( \
                    f'Applied endcaps: {"|".join(chosen)} -> {print_endcaps}' \
                    if self.dumb_terminal else \
                    f'Applied endcaps: { \
                            "|".join(chosen) \
                        } -> \033[93m{ \
                            print_endcaps[0:len(applied_endcaps[0])] \
                        }\033[0m{ \
                            print_endcaps[len(applied_endcaps[0]):len(print_endcaps) - len(applied_endcaps[-1])] \
                        }\033[93m{ \
                            print_endcaps[len(print_endcaps) - len(applied_endcaps[-1]):len(print_endcaps)]\
                        }\033[0m' \
                )
            else:
                print(f'{__program__}: endcaps not applied')

        applied_l33t: list[str] = super().apply_l33t(applied_endcaps)
        print_l33t: str = None
        if self.verbose:
            print_l33t = "|".join([i for i in applied_l33t if i != ''])
            if self.l33t_chance != 0 and applied_endcaps != applied_l33t:
                if self.dumb_terminal:
                    print(f'Applied L33T: {print_endcaps} -> {print_l33t}')
                else:
                    message: str = f'Applied L33T: {print_endcaps} -> '
                    for i in range(0, len(print_l33t)):
                        if print_l33t[i] != print_endcaps[i]:
                            message += f'\033[93m{print_l33t[i]}\033[0m'
                        else:
                            message += print_l33t[i]
                    print(message + '\033[0m')
            else: 
                print(f'{__program__}: L33T not applied')

        applied_seperators: list[str] = super().apply_seperators(applied_l33t)
        print_seperators: str = None
        if self.verbose:
            print_seperators = "|".join([i for i in applied_seperators if i != ''])
            if self.seperator_chance != 0 and applied_l33t != applied_seperators:
                if self.dumb_terminal:
                    print(f'Applied seperators: {print_l33t} -> {print_seperators}')
                else:
                    message: str = f'Applied seperators: {print_l33t} -> '
                    for i in range(0, len(applied_seperators)):
                        value: str = applied_seperators[i]
                        if len(value) > 0 and not(i in [0, len(applied_seperators) - 1]) and \
                            (value in self.SEPARATORS or re.findall(r'^[A-Z]', value[0]) != []):
                            message += f'\033[93m{value[0]}\033[0m{value[1:]}'
                        else:
                            message += value

                        if i < len(applied_seperators) - 2 and applied_seperators[i] != '':
                            message += '|'
                    print(message + '\033[0m')
            else: 
                print(f'{__program__}: seperators not applied')

        return ''.join(applied_seperators)

EPILOG_PHRASES: Final[tuple[str]] = (
    'rawr x3',
    'lolz@!!!',
    'rawr means i love you in dinosaur >:3',
    'haha! i\'m using my computer! :D'
)
# print epilog with italics instead of in quotes if terminal is ANSI/VT100-compatible
term = os.environ.get("TERM", "").lower()
parser_epilog = choice(EPILOG_PHRASES)
dumb_terminal = True
if sys.stdout.isatty() and (term or term != "dumb"):
    parser_epilog = f'\033[3m{parser_epilog}\033[0m'
    dumb_terminal = False
else:
    parser_epilog = f'"{parser_epilog}"'

# argparse stuff
parser = argparse.ArgumentParser(
    prog=__program__,
    description='Generates a random emo username.',
    epilog=parser_epilog
)
parser.add_argument(
    '-d', '--source',
    help="the source directory or file to pull names from (default: ../sources)",
    default=Path(f'{os.path.dirname(os.path.realpath(__file__))}/../sources'),
    type=Path,
    metavar='PATH'
)
parser.add_argument(
    '-e', '--endcaps',
    help="chance of including a random prefix and/or suffix, denoted as an integer from 0-100 (default: 33)",
    default=33,
    type=int,
    metavar='INT'
)
parser.add_argument(
    '-l', '--l33t',
    help="chance of changing a letter to its l33tspeak equivalent, denoted as an integer from 0-100 (default: 33)",
    default=33,
    type=int,
    metavar='INT'
)
parser.add_argument(
    '-s', '--seperator',
    help="chance of changing including word seperators, denoted as an integer from 0-100 (default: 33)",
    default=33,
    type=int,
    metavar='INT'
)
parser.add_argument(
    '--max',
    action='store_true',
    help="shortcut for '--endcaps 100 --l33t 100 --seperator 100'"
)
parser.add_argument(
    '--min',
    action='store_true',
    help="shortcut for '--endcaps 0 --l33t 0 --seperator 0'"
)
parser.add_argument(
    '-v', '--verbose',
    action='store_true',
    help="prints a walkthrough of how each string is transformed"
)
parser.add_argument(
    '--version',
    action='version',
    version=f'{__program__} {__version__}'
)
args = parser.parse_args()

if args.max and args.min:
    print(f'{__program__}: cannot have both max and min, dummy!')
    sys.exit(1)
if args.max:
    args.endcaps = 100
    args.l33t = 100
    args.seperator = 100
if args.min:
    args.endcaps = 0
    args.l33t = 0
    args.seperator = 0

print(
    __EmogenCLI(
        args.verbose,
        dumb_terminal,
        args.source,
        args.endcaps,
        args.l33t,
        args.seperator
    ).generate()
)
sys.exit()
