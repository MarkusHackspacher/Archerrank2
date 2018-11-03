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

from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy import Column

from PyQt5 import QtGui, QtCore, QtWidgets



class DlgSqlTable(QtWidgets.QDialog):
    """
    Dialog generate from sql table
    """
    def __init__(self, session, table):
        """Initial user interface and slots

        :returns: none
        """
        super(DlgSqlTable, self).__init__()
        self.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox(self)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Ok |
                                          QtWidgets.QDialogButtonBox.Cancel)
        self.boxLayout = QtWidgets.QBoxLayout(
            QtWidgets.QBoxLayout.TopToBottom, self)
        self.gridLayout = QtWidgets.QGridLayout()
        self.setWindowTitle(self.tr("Show Drawing"))

        print(session.query(table).all())
        print(dir(table))
        print(table.__dict__.items())

        def methods(cls):
            return [x for x, y in cls.__dict__.items() if type(y) == InstrumentedAttribute
                    and not 'id' in x and not 's' in x[-1]]

        methods = methods(table)

        self.labels = [QtWidgets.QLabel(self)
                                for _ in methods]
        for buttonnumber, label in enumerate(self.labels):
            #label.setMaximumSize(QtCore.QSize(58, 58))
            label.setAutoFillBackground(True)
            self.gridLayout.addWidget(
                label, buttonnumber, 1, 1, 1)
            label.setText(self.tr("Item {} {}".format(buttonnumber, methods[buttonnumber])))

        self.boxLayout.addLayout(self.gridLayout)
        self.boxLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.close)



    def values(self):
        """Values

        :return:
        """
        return (str('1'))



    @staticmethod
    def get_values(session, table):
        """static method to create the dialog and return
        (dialog.values, accepted)

        :param sysdat: Lotto setting
        :type sysdat: string
        :returns: dialog.values, accepted
        :rtype: array of int, bool
        """
        dialog = DlgSqlTable(session, table)
        result = dialog.exec_()
        return (dialog.values(), result == QtWidgets.QDialog.Accepted)
