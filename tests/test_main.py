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

import time
from unittest import TestCase

from modules import main, model


class arguments():
    log = 40
    database = ':memory:'
    language = 'en'


class ShowMainTestCase(TestCase):
    def setUp(self):
        """Creates the QApplication instance"""

        # Simple way of making instance a singleton
        super(ShowMainTestCase, self).setUp()
        self.app = main.Main(arguments())

    def tearDown(self):
        """Deletes the reference owned by self"""
        time.sleep(.2)
        self.app.ui.close()
        super(ShowMainTestCase, self).tearDown()
        time.sleep(.2)

    def test_onprint(self):
        """Test onprint"""
        self.app.onprint(test=True)

    def test_on_overview(self):
        self.app.on_overview(test=True)

    def test_showinfo(self):
        self.app.oninfo(test=True)

    def test_entry(self):
        self.app.entry_new(model.Bow, self.app.model_bow, test=True)
        self.assertEqual(self.app.model_bow.rowCount(self.app.model_bow), 1)
        index = self.app.model_bow.createIndex(0, 1)
        self.app.ui.tableView_bow.setCurrentIndex(index)
        time.sleep(.1)
        self.app.entry_edit(model.Bow, self.app.model_bow, test=True)
        time.sleep(.1)
        self.app.entry_delete(model.Bow, self.app.model_bow)
        self.assertEqual(self.app.model_bow.rowCount(self.app.model_bow), 0)

    def test_entry_user(self):
        self.app.entry_new(model.Age, self.app.model_age, test=True)
        time.sleep(.1)
        self.app.entry_new(model.Bow, self.app.model_bow, test=True)
        time.sleep(.1)
        self.app.entry_new(model.Club, self.app.model_club, test=True)
        time.sleep(.1)
        self.app.entry_new(model.User, self.app.model_user, test=True)
        time.sleep(.1)
        self.assertEqual(self.app.model_user.rowCount(self.app.model_bow), 1)
        index = self.app.model_user.createIndex(0, 1)
        self.app.ui.tableView_user.setCurrentIndex(index)
        self.app.entry_edit(model.User, self.app.model_user, test=True)
        time.sleep(.1)

    def test_entry_club(self):
        time.sleep(.1)
        self.app.entry_new(model.Club, self.app.model_club, test=True)
        self.assertEqual(self.app.model_club.rowCount(self.app.model_club), 1)
        index = self.app.model_club.createIndex(0, 1)
        self.app.ui.tableView_club.setCurrentIndex(index)
        time.sleep(.1)
        self.app.entry_edit(model.Club, self.app.model_club, test=True)
        time.sleep(.1)
