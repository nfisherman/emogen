#!/usr/bin/env python3

import argparse, os, sys
from mimetypes import guess_type
from pathlib import Path
from typing import Final
from random import randrange, choice

NAME: Final[str] = 'emogen'
VERSION: Final[tuple[int]] = (0, 1, 0)

class EmoGen:
    PREFIX_SUFFIX: Final[tuple[tuple[str]]] = (
        ('', '_'),
        ('_', '_'),
        (
            ('_xx', 'xx_'),
            ('_xX', 'Xx_'),
            ('xx', 'xx'),
            ('xX', 'Xx')
        )
    )
    SEPARATORS: Final[tuple[str]] = ('_', 'CAP')
    L33T: Final[dict[str, str]] = {
        "A": "4",
        # "B": "8",
        "E": "3",
        # "G": "9",
        "O": "0",
        "S": "5"
    }

    def __init__(self, data_source: Path, prefix_chance: int = 3, l33t_chance: int = 3, seperator_chance: int = 2):
        self.data: list[list[str]] = list()
        self.set_data_source(data_source)
        self.prefix_chance = prefix_chance
        self.l33t_chance = l33t_chance
        self.seperator_chance = seperator_chance

    def __str__(self) -> str:
        result: list[str] = list()

        for name in self.data:
            result.append(''.join(name))

        return str(result)

    def set_data_source(self, data_source: Path) -> bool:
        self.data: list[list[str]] = list()

        for child in data_source.iterdir():
            if guess_type(child)[0] == 'text/plain':
                with open(child, 'r') as source:
                    for line in source:
                        if line[:1] in ('', '#', '/', '%', ';', '\n'):
                            continue

                        seperated_line: list[str] = line.split('|')
                        seperated_line[-1] = seperated_line[-1].strip(' \n\r')

                        self.data.append(seperated_line)

        if len(self.data) == 0:
            self.data = None

        return self.data is not None

    def generate(self) -> str:
        result: str = ''

        end_caps: tuple = ('', '')
        if self.prefix_chance <= 0 or randrange(self.prefix_chance):  # (default) 50% chance of prefix & suffix
            end_caps = choice(self.PREFIX_SUFFIX)
            if type(end_caps[0]) is tuple:
                end_caps = choice(end_caps)

            result += end_caps[0]

        user: list[str] = choice(self.data)
        for i in range(len(user)):
            if self.l33t_chance <= 0 or randrange(self.l33t_chance):  # (default) 50% chance of l33t
                for j in list(range(len(user[i])))[1:]:
                    if (user[i][j].upper() in self.L33T.keys()
                            and (self.l33t_chance <= 0 or randrange(self.l33t_chance*12))):
                        user[i] = user[i][:j] + self.L33T[user[i][j].upper()] + user[i][j+1:]
                        break

        if self.seperator_chance <= 0 or randrange(self.seperator_chance):  # (default) 50% chance of having seperator
            seperator = choice(self.SEPARATORS)
            match seperator:
                case "CAP":
                    for i in range(len(user)):
                        user[i] = user[i][0].upper() + user[i][1:]

                    result = ''.join(user)
                case _:
                    result = seperator.join(user)
        else:
            result = ''.join(user)

        return end_caps[0] + result + end_caps[1]

if __name__ == '__main__':
    EPILOG_PHRASES: Final[tuple[str]] = (
        'rawr x3',
        'lolz@!!!',
        'rawr means i love you in dinosaur >:3',
        'haha! i\'m using my computer! :D'
    )
    # print epilog with italics instead of in quotes if terminal is ANSI-compatible
    term = os.environ.get("TERM", "").lower()
    parser_epilog = choice(EPILOG_PHRASES)
    if sys.stdout.isatty() and (term or term != "dumb"):
        parser_epilog = f'\033[3m{parser_epilog}\033[0m'
    else:
        parser_epilog = f'"{parser_epilog}"'

    parser = argparse.ArgumentParser(
        prog=NAME,
        description='Generates a random emo username.',
        epilog=parser_epilog
    )
    parser.add_argument(
        '-d', '--source',
        help="the source directory or file to pull names from (default: .../emogen/sources/)",
        default=Path(f'{os.path.dirname(os.path.realpath(__file__))}/sources'),
        type=Path
    )
    parser.add_argument(
        '--version',
        action='store_true',
        help="prints software version and exits"
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help="prints a walkthrough of how each string is transformed, for debugging purposes"
    )
    args = parser.parse_args()

    if args.version:
        print(f'{NAME} {".".join(str(i) for i in VERSION)}')
        sys.exit()

    emo_gen: EmoGen = EmoGen(args.source)
    print(emo_gen.generate())
