#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__author__ = 'nfisherman'
__copyright__ = 'Copyright (c) 2026 nfisherman'
__license__ = '0BSD'
__version__ = '1.0.0'
__status__ = "Production"

import argparse, os, sys
from pathlib import Path
from mimetypes import guess_type

try:
    sys.argv[1]
except IndexError:
    sys.argv.append('')

prog: str = os.path.basename(Path(sys.argv[0]))
parser = argparse.ArgumentParser(
    prog=prog,
    description='Installs emogen.'
)
parser.add_argument(
    'dest',
    help='directory or file to install to'
)
parser.add_argument(
    '--version',
    action='version',
    version=f'{prog} {__version__}'
)
args = parser.parse_args()

while args.dest == '':
    temp = input('Install Location: ').strip()
    if temp != '':
        args.dest = Path(temp)
else:
    args.dest = Path(args.dest)

src: Path = Path(f'{os.path.dirname(os.path.realpath(__file__))}/src/_cli.py')
if not(os.path.isfile(src)):
    print(f'{sys.argv[0]}: {src} could not be found')
    sys.exit(1)

if \
   os.path.isdir(args.dest) or \
   str(args.dest)[-1] in ['/', '\\'] or \
   (len(os.path.basename(args.dest).split('.')) == 1 and guess_type(args.dest)[0] == None):
    args.dest = os.path.join(args.dest, 'emogen')
try:
    os.makedirs(os.path.dirname(args.dest))
except FileExistsError:
    pass

if os.path.exists(args.dest):
    os.remove(args.dest)
os.chmod(src, 0o001)
os.symlink(src, args.dest)
print(f'{sys.argv[0]}: installed emogen to {args.dest}')
