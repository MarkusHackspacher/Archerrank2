#!/usr/bin/env python3
#  -*- coding: utf-8 -*-

"""
Archerank2

Copyright (C) <2018> Markus Hackspacher

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
import sys

from modules import main


def onopen(self):
    """open file

    :return:
    """
    fname = QtWidgets.QFileDialog.getOpenFileName(self.ui, 'Open file',
                                                  '.', "SQLite files (*.sqlite)")
    print(fname)


def onnew(self):
    """save as file

    :return:
    """
    fname = QtWidgets.QFileDialog.getSaveFileName(self.ui, 'New file',
                                                  '.', "SQLite files (*.sqlite)")
    print(fname)


if __name__ == "__main__":
    app = main.Main(sys.argv)
    app.main_loop()
