#!/usr/bin/env python3
# -*- coding: utf-8 -*-

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

import sqlite3
import sys
from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askopenfilename

"""Read an Archerrank .sqlite file"""
my_file = Path('')
if len(sys.argv) >= 2:
    my_file = Path(sys.argv[1])
if my_file.is_file():
    filename = str(my_file)
else:
    Tk().withdraw()  # we don't want a full GUI, so keep the root window from appearing
    filename = askopenfilename(title="select file",
        filetypes=(("sqlite files", "*.sqlite"), ("all files", "*.*")))
    # show an "Open" dialog box and return the path to the selected file

print(filename)
conn = sqlite3.connect(filename)

c = conn.cursor()
#for row in c.execute('SELECT * FROM results ORDER BY score, kills'):
for row in c.execute('SELECT * FROM sqlite_master'):    
    
    print(row)
    
    
conn.close()
