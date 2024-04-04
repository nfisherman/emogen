#!/usr/bin/python3

import argparse
from mimetypes import guess_type
from pathlib import Path
from typing import Final
from random import randrange


class EmoGen:
    PREFIX_SUFFIX: Final[tuple[tuple[str]]] = (
        ('', '_'),
        ('_', '_'),
        ('_xx', 'xx_'),
        ('_xX', 'Xx_'),
        ('xx', 'xx'),
        ('xX', 'Xx')
    )
    SEPARATORS: Final[tuple[str]] = ('_', 'CAP')
    LETTER_NUMBER: Final[dict[str, str]] = {
        "A": "4",
        "B": "8",
        "E": "3",
        "G": "9",
        "O": "0",
        "S": "5"
    }

    def __init__(self, data_source: Path):
        self.data = None
        self.set_data_source(data_source)

    def __str__(self) -> str:
        result: list[str] = list()

        for name in self.data.keys():
            result.append(name)

        return str(result)

    def set_data_source(self, data_source: Path) -> bool:
        self.data: dict[str, list[str]] = dict()

        for child in data_source.iterdir():
            if guess_type(child)[0] == 'text/plain':
                with open(child, 'r') as source:
                    for line in source:
                        if line[:1] in ('', '#', '/', '%', ';', '\n'):
                            continue

                        seperated_line: list[str] = line.split('|')
                        seperated_line[-1] = seperated_line[-1].strip(' \t\n\r')

                        self.data.update({''.join(seperated_line): seperated_line})

        if len(self.data) == 0:
            self.data = None

        return self.data is not None

    def generate(self) -> str:
        result: str = str()

        prefix = None
        if randrange(2):
            prefix = randrange(len(self.PREFIX_SUFFIX))
            str += self.PREFIX_SUFFIX[prefix][0]


if __name__ == '__main__':
    emo_gen: EmoGen = EmoGen(Path('sources'))
