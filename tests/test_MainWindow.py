# -*- coding: utf-8 -*-

"""
Archerank2

Copyright (C) <2019,2023> Markus Hackspacher

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

import unittest
from modules.gui.mainwindow import Ui_MainWindow


class TestMainWindow(unittest.TestCase):

    def test_main_window(self):
        # Create a new Ui_MainWindow object
        ui = Ui_MainWindow()

        # Check that the window title is correct
        self.assertEqual(ui.centralwidget.windowTitle(), "Archerrank2")

        # Check that the label text is correct
        self.assertEqual(ui.label_user.text(), "participants")

        # Check that the push button text is correct
        self.assertEqual(ui.pushButton_user.text(), "add new user")
        self.assertEqual(ui.pushButton_edituser.text(), "edit user")
        self.assertEqual(ui.pushButton_deleteuser.text(), "delete user")

        # Check that the menu items are correct
        self.assertEqual(ui.menuFile.title(), "&File")
        self.assertEqual(ui.menuInfo.title(), "I&nfo")
        self.assertEqual(ui.menuEvaluation.title(), "E&valuation")

        # Check that the action text is correct
        self.assertEqual(ui.actionExit.text(), "&Exit")
        self.assertEqual(ui.actionOpen.text(), "&Open")
        self.assertEqual(ui.actionSave.text(), "&Save")
        self.assertEqual(ui.actionNew.text(), "&New")
        self.assertEqual(ui.actionInfo.text(), "&Info")
        self.assertEqual(ui.actionOverview.text(), "&Overview")
        self.assertEqual(ui.actionPrintPreview.text(), "&Print Preview")
        self.assertEqual(ui.actionLoad_file.text(), "&Load file")
        self.assertEqual(ui.actionSave_file_as.text(), "&Save file as")
        self.assertEqual(ui.actionCreateCertificates.text(), "&Create certificates")
        self.assertEqual(ui.actionXLSX_Export.text(), "XLSX Export")
        self.assertEqual(ui.actionCreateAddress.text(), "Create Address")


if __name__ == "__main__":
    unittest.main()
