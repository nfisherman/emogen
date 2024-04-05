#!/usr/bin/python3

import argparse
from mimetypes import guess_type
from pathlib import Path
from typing import Final
from random import randrange, choice


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
    LETTER_NUMBER: Final[dict[str, str]] = {
        "A": "4",
        # "B": "8",
        "E": "3",
        # "G": "9",
        "O": "0",
        "S": "5"
    }

    def __init__(self, data_source: Path):
        self.data: list[list[str]] = list()
        self.set_data_source(data_source)

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

    def generate(self, prefix_chance: int = 3, l33t_chance: int = 3, seperator_chance: int = 2) -> str:
        result: str = ''

        end_caps: tuple = ('', '')
        if prefix_chance <= 0 or randrange(prefix_chance):  # (default) 50% chance of prefix & suffix
            end_caps = choice(self.PREFIX_SUFFIX)
            if type(end_caps[0]) is tuple:
                end_caps = choice(end_caps)

            result += end_caps[0]

        user: list[str] = choice(self.data)

        for i in range(len(user)):
            if l33t_chance <= 0 or randrange(l33t_chance):  # (default) 50% chance of l33t
                for j in list(range(len(user[i])))[1:]:
                    if (user[i][j].upper() in self.LETTER_NUMBER.keys()
                            and (l33t_chance <= 0 or randrange(l33t_chance*12))):
                        user[i] = user[i][:j] + self.LETTER_NUMBER[user[i][j].upper()] + user[i][j+1:]
                        break

        if seperator_chance <= 0 or randrange(seperator_chance):  # (default) 50% chance of having seperator
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
    emo_gen: EmoGen = EmoGen(Path('sources'))
    print(emo_gen.generate())
