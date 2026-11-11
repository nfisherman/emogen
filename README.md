# emogen

A python command-line utility to generate a random emo username.

## Dependencies

Python > 3.10

## Install

1. Make sure ``install.py`` is executable.

    ```sh
    $ chmod +x install.py
    ```

2. Run ``install.py`` and provide an install location!

    ```sh
    $ ./install.py
    Install Location: ~/opt/bin
    ./install.py: installed emogen to ./emogen
    ```

    or...

    ```sh
    $ ./install.py ~/opt/bin
    ./install.py: installed emogen to ./emogen
    ```

## Usage

### From the command line

```sh
$ emogen --help
usage: emogen [-h] [-d PATH] [-e INT] [-l INT] [-s INT] [--max] [--min] [-v]
              [--version]

Generates a random emo username.

options:
  -h, --help           show this help message and exit
  -d, --source PATH    the source directory or file to pull names from
                       (default: ../sources)
  -e, --endcaps INT    chance of including a random prefix and/or suffix,
                       denoted as an integer from 0-100 (default: 33)
  -l, --l33t INT       chance of changing a letter to its l33tspeak
                       equivalent, denoted as an integer from 0-100 (default:
                       33)
  -s, --seperator INT  chance of changing including word seperators, denoted
                       as an integer from 0-100 (default: 33)
  --max                shortcut for '--endcaps 100 --l33t 100 --seperator 100'
  --min                shortcut for '--endcaps 0 --l33t 0 --seperator 0'
  -v, --verbose        prints a walkthrough of how each string is transformed
  --version            show program's version number and exit

"lolz@!!!"
$ emogen
_itw4sntaphasem0m_
$ emogen --max
_R3qui3mF0rMyChildh00dB3dr00m
```

### As a library

```python3
>>> import emogen, pathlib
>>> emogen = emogen.Emogen(pathlib.Path('../sources'))
>>> for i in range(5):
...     emogen.endcaps_chance = 10 * i
...     emogen.l33t_chance = 10 * i
...     emogen.seperator_chance = 10 * i
...     print(emogen.generate())
...
prozacprincess
mrsbrightside_
suffering5adgirl
4b4nd0nedangel
_xxeternalsadne5sbrig4de
```

## References

[1] M. Burford, “100+ Catchy Emo Usernames,” Thought Catalog. Accessed: Apr. 03, 2024. [Online]. Available: <https://thoughtcatalog.com/molly-burford/2022/01/100-emo-usernames-for-social-media/> [Archived: <https://web.archive.org/web/20240404030841/https://thoughtcatalog.com/molly-burford/2022/01/100-emo-usernames-for-social-media/>]
