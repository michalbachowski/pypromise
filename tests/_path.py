#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys
import argparse

def arg_parser(parser=None):
    if parser is None:
        parser = argparse.ArgumentParser(description='Path config.')
    parser.add_argument('-f', '--fix', action='store_true', dest='fix', \
        help='Fix path to tested modules')
    parser.add_argument('--debug', action='store_true', dest='debug', \
        help='Run in debug mode')
    return parser

def fix():
    if arg_parser().parse_args().fix:
        do_fix()

def do_fix():
    p = os.path.join(os.path.dirname(__file__), '../src/')
    if p not in sys.path:
        sys.path.insert(0, p)

if "__main__" == __name__:
    fix()
