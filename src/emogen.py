#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
emogen.py

Generates a random emo username with a configurable percentage chance
of randomization.
"""

__author__ = 'nfisherman'
__copyright__ = 'Copyright (c) 2026 nfisherman'
__credits__ = 'See "References" in README.md'
__license__ = '0BSD'
__version__ = '1.0.0'
__status__ = "Production"

import os, re, sys
from mimetypes import guess_type
from pathlib import Path
from typing import Final
from random import randrange, choice

class Emogen:
    """
    An emo name generator.
    """
    PREFIX_SUFFIX: Final[tuple[tuple[str]]] = (
        ('_', '_'),
        ('_xx', 'xx_'),
        ('xx', 'xx')
    )
    SEPARATORS: Final[tuple[str]] = ('_', 'CAP') # 'CAP' = capital letters
    L33T: Final[dict[str, str]] = {
        "A": "4",
        # "B": "8",
        "E": "3",
        # "G": "9",
        "O": "0",
        "S": "5"
    }

    def __init__(self,
            data_source: Path,
            endcaps_chance: int = 0,
            l33t_chance: int = 0,
            seperator_chance: int = 0):
        """
        Instantiates an emo name generator.

        Args:
            data_source (Path): the directory or text file to pull 
                                names from
            endcaps_chance (int): chance of including a random prefix 
                                  and suffix, denoted as an integer 
                                  from 0-100
            l33t_chance (int): chance of changing a letter to its 
                               l33tspeak equivalent, denoted as an 
                               integer from 0-100
            seperator_chance (int): chance of changing including word 
                                    seperators, denoted as an integer 
                                    from 0-100
        """
        self.set_data_source(data_source)
        self.endcaps_chance = endcaps_chance
        self.l33t_chance = l33t_chance
        self.seperator_chance = seperator_chance

    def __str__(self) -> str:
        result: list[str] = list()

        for name in self.data:
            result.append(''.join(name))

        return str(result)

    def _roll100(self, chance: int) -> bool:
        if chance < 0 or chance > 100:
            raise IndexError(f"Chance '{chance}' out of range 0:100")
        
        return chance != 0 and randrange(100) < chance

    def set_data_source(self, data_source: Path) -> bool:
        """
        Stores the data source in a way that is readable by the program
        (list[list[str]]).

        Args:
            data_source (Path): the data to pull from, can be either a
                                directory or a single text file

        Returns:
            bool: True, if operation has completed successfully
        """
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

    def apply_endcaps(self, data: list[str]) -> list[str]:
        """
        Apply endcaps to the inputted data.

        Args:
            data (list[str]): the data to transform
        
        Returns:
            list[str]: the transformed data
        """
        if len(data) == 0:
            raise IndexError('data cannot be blank')

        result: list[str] = data.copy()
        endcaps: list[str] = ['', '']
        if self._roll100(self.endcaps_chance):
            endcaps = list(choice(self.PREFIX_SUFFIX))
            # 1/3rd chance to remove prefix, suffix, or neither
            match randrange(0, 3):
                case 0:
                    # remove prefix
                    endcaps[0] = ''
                case 1:
                    # remove suffix
                    endcaps[1] = ''
                # case 2 include both 

            size: int = len(endcaps[0])
            # flip a coin for capitalization
            if randrange(0, 2) == 0:
                if size > 1:
                    if endcaps[0] != '':
                        endcaps[0] = endcaps[0][:size-1] + endcaps[0][-1].capitalize()
                    if endcaps[1] != '':
                        endcaps[1] = endcaps[1][0].capitalize() + endcaps[1][1:size]
                else:
                    if endcaps[0] != '':
                        endcaps[0] = endcaps[0].capitalize()
                    if endcaps[1] != '':
                        endcaps[1] = endcaps[1].capitalize()
            
        result.insert(0, endcaps[0])
        result.insert(len(result), endcaps[1])
        return result

    def apply_l33t(self, data: list[str]) -> list[str]:
        """
        Apply l33tspeak to the inputted data.

        Args:
            data (list[str]): the data to transform
        
        Returns:
            list[str]: the transformed data
        """
        if len(data) == 0:
            raise IndexError('data cannot be blank')

        result: list[str] = data.copy()

        # do not include endcaps if present
        observation_range: list[int] = \
            [1, len(data) - 1] \
            if (data[0], data[-1]) in self.PREFIX_SUFFIX else \
            [0, len(data)]
        for i in range(observation_range[0], observation_range[1]):
                term: str = result[i]
                # do not include seperators if present
                if term in self.SEPARATORS:
                    continue

                result[i] = ''
                for character in term:
                    uppercase: str = character.upper()
                    if uppercase in self.L33T.keys() and self._roll100(self.l33t_chance):
                        result[i] += self.L33T[uppercase]
                        continue
                    result[i] += character
        
        return result

    def apply_seperators(self, data: list[str]) -> list[str]:
        """
        Apply seperators to the inputted data.

        Args:
            data (list[str]): the data to transform
        
        Returns:
            list[str]: the transformed data
        """
        if len(data) == 0:
            raise IndexError('data cannot be blank')

        # do not include endcaps if present
        endcaps_flag: bool = \
            data[0].lower() in (i[0] for i in self.PREFIX_SUFFIX) or \
            data[-1].lower() in (i[1] for i in self.PREFIX_SUFFIX)
        result: list[str] = \
            data.copy()[1:len(data) - 1] \
            if endcaps_flag else \
            data.copy()

        if self._roll100(self.seperator_chance):
            seperator = choice(self.SEPARATORS)
            match seperator:
                case "CAP":
                    for i in range(0, len(result)):
                        if len(result[i]) != 0:
                            result[i] = result[i][0].capitalize() + result[i][1:]
                case _:
                    size: int = len(result)
                    for i in reversed(range(1, size)):
                        result.insert(i, seperator)
        
        return [data[0]] + result + [data[-1]] if endcaps_flag else result
                
    def choose_name(self) -> list[str]:
        """
        Return a random name from the data source.

        Returns:
            list[str]: a processed random name from the data source
        """

        return choice(self.data)

    def generate(self) -> str:
        """
        Generate an emo name using all random transformations.

        Returns:
            str: an emo name
        """
        result: str = self.choose_name()

        result = self.apply_endcaps(result)
        result = self.apply_l33t(result)
        result = self.apply_seperators(result)

        return ''.join(result)
