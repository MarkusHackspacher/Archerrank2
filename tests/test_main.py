# -*- coding: utf-8 -*-

"""
Archerank2

Copyright (C) <2019> Markus Hackspacher

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

from unittest import TestCase

from modules import main


class arguments():
    log = 40
    database = ':memory:'
    language = 'de'


class ShowMainTestCase(TestCase):
    def setUp(self):
        """Creates the QApplication instance"""

        # Simple way of making instance a singleton
        super(ShowMainTestCase, self).setUp()
        self.app = main.Main(arguments())

    def tearDown(self):
        """Deletes the reference owned by self"""
        self.app.ui.close()
        del self.app
        super(ShowMainTestCase, self).tearDown()

    def test_onprint(self):
        self.app.onprint(test=True)

    def test_on_overview(self):
        self.app.on_overview(test=True)

    def test_showinfo(self):
        self.app.oninfo(test=True)
