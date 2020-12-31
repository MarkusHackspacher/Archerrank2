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

from modules import main, model

_instance = None


class arguments():
    log = 40
    database = ':memory:'
    language = 'en'


class ShowMainTestCase(TestCase):
    def setUp(self):
        """Creates the QApplication instance"""

        # Simple way of making instance a singleton
        super(ShowMainTestCase, self).setUp()
        global _instance
        if _instance is None:
            _instance = main.Main(arguments())

        self.app = _instance


    def tearDown(self):
        """Deletes the reference owned by self"""
        self.app.dialog.ui.close()
        super(ShowMainTestCase, self).tearDown()

    def test_onprint(self):
        """Test onprint"""
        self.app.dialog.onprint(test=True)

    def test_on_overview(self):
        self.app.dialog.on_overview(test=True)

    def test_showinfo(self):
        self.app.dialog.oninfo(test=True)

    def test_entryBow(self):
        self.app.dialog.entry_new(model.Bow, self.app.model_bow, test=True)
        self.assertEqual(self.app.model_bow.rowCount(), 1)
        index = self.app.model_bow.createIndex(0, 1)
        self.app.dialog.ui.tableView_bow.setCurrentIndex(index)
        self.app.dialog.entry_edit(model.Bow, self.app.model_bow, test=True)
        self.app.dialog.entry_delete(model.Bow, self.app.model_bow)
        self.assertEqual(self.app.model_bow.rowCount(), 0)

    def test_entryUser(self):
        self.app.dialog.entry_new(model.Age, self.app.model_age, test=True)
        self.app.dialog.entry_new(model.Bow, self.app.model_bow, test=True)
        self.app.dialog.entry_new(model.Club, self.app.model_club, test=True)
        self.app.dialog.entry_new(model.User, self.app.model_user, test=True)
        self.assertEqual(self.app.model_age.rowCount(), 1)
        self.assertEqual(self.app.model_user.rowCount(), 1)
        index = self.app.model_user.createIndex(0, 1)
        self.app.dialog.ui.tableView_user.setCurrentIndex(index)
        self.app.dialog.entry_edit(model.User, self.app.model_user, test=True)

    def test_entryClub(self):
        self.app.dialog.entry_new(model.Club, self.app.model_club, test=True)
        self.assertEqual(self.app.model_club.rowCount(), 1)
        index = self.app.model_club.createIndex(0, 1)
        self.app.dialog.ui.tableView_club.setCurrentIndex(index)
        self.app.dialog.entry_edit(model.Club, self.app.model_club, test=True)
        self.app.dialog.entry_delete(model.Club, self.app.model_club)
        self.assertEqual(self.app.model_club.rowCount(), 0)

