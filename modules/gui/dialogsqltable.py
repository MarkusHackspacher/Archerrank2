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
from modules.ext.alchemical_model import SqlAlchemyTableModel




class DlgSqlTable(QtWidgets.QDialog):
    """
    Dialog generate from sql table
    """
    def __init__(self, session, table, model):
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

        methods = [m.key for m in table.__table__.columns if not len(m.key) == 2]

        self.labels = [QtWidgets.QLabel(self) for _ in methods]
        self.field = {}
        for buttonnumber, name in enumerate(methods):
            if name in ('name', 'short', 'lastname', 'other'):
                self.field[name] = QtWidgets.QLineEdit(self)
            elif name in ('killpt', 'sorting', 'score', 'part', 'rate', 'sep', 'adult'):
                self.field[name] = QtWidgets.QSpinBox(self)
            elif name in ('club_id'):
                self.field[name] = QtWidgets.QComboBox(self)
                model_club = SqlAlchemyTableModel(session, model.Club, [('Name', model.Club.name, "name", {"editable": True}),])
                self.field[name].setModel(model_club)
            elif name in ('bow_id'):
                self.field[name] = QtWidgets.QComboBox(self)
                model_bow = SqlAlchemyTableModel(session, model.Bow, [('Name', model.Bow.name, "name", {"editable": True}),])
                self.field[name].setModel(model_bow)
            elif name in ('age_id'):
                self.field[name] = QtWidgets.QComboBox(self)
                self.model_age = SqlAlchemyTableModel(session, model.Age, [('Name', model.Age.name, "name", {"editable": True}),
                                                                      ('Id', model.Age.id, "id", {"editable": False})])
                self.field[name].setModel(self.model_age)



            else:
                self.field[name] = QtWidgets.QComboBox(self)

            self.gridLayout.addWidget(
                self.field[name], buttonnumber, 2, 1, 1)

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
        for name in self.field:
            if name in ('name', 'short', 'lastname', 'other'):
                print(name, self.field[name].text())
            elif name in ('age_id'):
                print(name, self.field[name].currentIndex())
                print(self.model_age.data(0, 0))
        return (str('d'))



    @staticmethod
    def get_values(session, table, model):
        """static method to create the dialog and return
        (dialog.values, accepted)

        :param sysdat: Lotto setting
        :type sysdat: string
        :returns: dialog.values, accepted
        :rtype: array of int, bool
        """
        dialog = DlgSqlTable(session, table, model)
        result = dialog.exec_()
        return (dialog.values(), result == QtWidgets.QDialog.Accepted)