#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
release.py

Packages files for release.
"""

__author__ = 'nfisherman'
__copyright__ = 'Copyright (c) 2026 nfisherman'
__license__ = '0BSD'
__version__ = '0.1.0'
__status__ = "Development"

import argparse, glob, os, sys, timeit, tarfile
from zipfile import ZipFile
from mimetypes import guess_type
from pathlib import Path

prog: str = os.path.basename(Path(sys.argv[0]))
parser = argparse.ArgumentParser(
    prog=prog,
    description='Packages files for release.'
)
parser.add_argument(
    'name',
    help='name of program',
    type=str
)
parser.add_argument(
    'version',
    help='version to save as',
    type=str
)
parser.add_argument(
    '-d', '--source',
    help='directory to work in (default: ./)',
    type=Path,
    default=Path('.')
)
parser.add_argument(
    '-o', '--output',
    help='output directory (default: release/)',
    type=Path,
    default=Path('release')
)
parser.add_argument(
    '-f', '--file', 
    action="extend", 
    nargs="+",
    help='file(s) to check for patterns to match and add to archive (default: util/includes.txt)',
    type=Path,
    default=[Path(f'{os.path.dirname(os.path.realpath(__file__))}/includes.txt')]
)
parser.add_argument(
    '-v', '--verbose',
    action='store_true',
    help="prints extra information"
)
parser.add_argument(
    '--version',
    action='version',
    version=f'{prog} {__version__}'
)
args = parser.parse_args()

def __log(message: str):
    if args.verbose:
        print(message)

includes: list[str] = []
for file in args.file:
    if guess_type(file)[0] == 'text/plain':
        with open(Path(file), 'r') as f:
            for line in f:
                includes.append(line.strip())

# make zip
time_start = timeit.default_timer()
zip_path: Path = Path(f'{args.output}/{args.version}/{args.name}-{args.version}.zip')
try:
    os.makedirs(os.path.dirname(zip_path))
except FileExistsError:
    pass

if os.path.exists(zip_path):
    os.remove(zip_path)
with ZipFile(zip_path, 'w') as archive:
    for pattern in includes:
        for file in glob.glob(pattern, recursive=True):
            archive.write(file)
time_end_zip = timeit.default_timer()
__log(f'{sys.argv[0]}: bundled zip at {zip_path} ({time_end_zip - time_start:.3f}s)')

# make tar
tar_path: Path = Path(f'{args.output}/{args.version}/{args.name}-{args.version}.tar.gz')
if os.path.exists(tar_path):
    os.remove(tar_path)
with tarfile.open(tar_path, 'w:gz') as archive:
    for pattern in includes:
        for file in glob.glob(pattern, recursive=True):
            archive.add(file)
time_end = timeit.default_timer()
__log(f'{sys.argv[0]}: bundled tar at {tar_path} ({time_end - time_end_zip:.3f}s)')

sys.exit(0)
