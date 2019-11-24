# -*- coding: utf-8 -*-

"""
Archerank2

Copyright (C) <2018-2019> Markus Hackspacher

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

from openpyxl import Workbook


class writexlsx:
    def __init__(self):
        self.wb = Workbook()
        self.wsWinner = self.wb.active
        self.wsWinner.title = "winner"
        self.wsAddress = self.wb.create_sheet("address")

    def save(self, filename):
        self.wb.save(filename)

    def winner(self, data):
        """write winner data in sheet"""
        self.wsWinner.append(data)

    def adresse(self, data):
        """write adresse data in sheet"""
        self.wsAddress.append(data)
