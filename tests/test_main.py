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
from unittest import skip, TestCase

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
        self.dialog = main.ArcherrankDialog(self.app)

    def tearDown(self):
        """Deletes the reference owned by self"""
        # self.app.quit()
        del self.app
        super(ShowMainTestCase, self).tearDown()

    # @skip("Test onprint")
    def test_onprint(self):
        """Test onprint"""
        self.dialog.onprint(test=True)

    # @skip("Test overview")
    def test_on_overview(self):
        self.dialog.on_overview(test=True)

    # @skip("Test showinfo")
    def test_showinfo(self):
        self.dialog.oninfo(test=True)

    #@skip("entry_Bow")
    def test_entryBow(self):
        self.dialog.entry_new(model.Bow, self.app.model_bow, test=True)
        self.assertEqual(self.app.model_bow.rowCount(self.app.model_bow), 1)
        index = self.app.model_bow.createIndex(0, 1)
        self.dialog.ui.tableView_bow.setCurrentIndex(index)
        self.dialog.entry_edit(model.Bow, self.app.model_bow, test=True)
        self.dialog.entry_delete(model.Bow, self.app.model_bow)
        self.assertEqual(self.app.model_bow.rowCount(self.app.model_bow), 0)

    #@skip("entry_user")
    def test_entryUser(self):
        self.dialog.entry_new(model.Age, self.app.model_age, test=True)
        self.dialog.entry_new(model.Bow, self.app.model_bow, test=True)
        self.dialog.entry_new(model.Club, self.app.model_club, test=True)
        self.dialog.entry_new(model.User, self.app.model_user, test=True)
        self.assertEqual(self.app.model_user.rowCount(self.app.model_bow), 1)
        index = self.app.model_user.createIndex(0, 1)
        self.dialog.ui.tableView_user.setCurrentIndex(index)
        self.dialog.entry_edit(model.User, self.app.model_user, test=True)

    #@skip("entry_Club")
    def test_entryClub(self):
        self.dialog.entry_new(model.Club, self.app.model_club, test=True)
        self.assertEqual(self.app.model_club.rowCount(self.app.model_club), 1)
        index = self.app.model_club.createIndex(0, 1)
        self.dialog.ui.tableView_club.setCurrentIndex(index)
        self.dialog.entry_edit(model.Club, self.app.model_club, test=True)
        self.dialog.entry_delete(model.Club, self.app.model_club)
        self.assertEqual(self.app.model_club.rowCount(self.app.model_club), 0)

