#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
Archerank2

Copyright (C) <2018-2022> Markus Hackspacher

This file is part of Archerank2.

Archerank2 is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Archerank2 is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Lesser General Public License for more details.

You should have received a copy of the GNU General Public License
along with Archerank2.  If not, see <http://www.gnu.org/licenses/>.
"""
import argparse

from modules import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-db', '--database', help='file of the database')
    parser.add_argument('-l', '--language', help='ISO code of language, de for Germany')
    parser.add_argument('-log', type=int, help='logging level', choices=[1, 2, 3, 4, 5], default=3)
    args = parser.parse_args()
    app = main.Main(args)
    app.main_loop()
