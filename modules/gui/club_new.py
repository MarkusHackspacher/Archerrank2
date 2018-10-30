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

import sys
import os
from os.path import join


from PyQt5 import QtGui, QtCore, QtWidgets, uic



class DlgNewClub(QtWidgets.QDialog):
    """
    New Club window
    """
    def __init__(self):
        """Initial user interface and slots

        :returns: none
        """
        super(DlgNewClub, self).__init__()
        self.ui = uic.loadUi(os.path.abspath(os.path.join(
            os.path.dirname(sys.argv[0]),
            "modules", "gui", "club_new.ui")))
        self.ui.exec_()
