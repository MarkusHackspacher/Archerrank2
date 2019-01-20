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

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import Qt
from sqlalchemy import Column
from sqlalchemy.orm.attributes import InstrumentedAttribute

from modules.ext.alchemical_model import SqlAlchemyTableModel


class DlgSqlTable(QtWidgets.QDialog):
    STRING = ('name', 'short', 'lastname', 'other', 'email', 'address')
    INT = ('killpt', 'sorting', 'score', 'part', 'rate', 'sep', 'adult', 'payment', 'advertising')

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
            if name in self.STRING:
                self.field[name] = QtWidgets.QLineEdit(self)
            elif name in self.INT:
                self.field[name] = QtWidgets.QSpinBox(self)
            elif name in 'club_id':
                self.field[name] = QtWidgets.QComboBox(self)
                self.model_club = self.my_table_model(model.Club, session)
                self.field[name].setModel(self.model_club)
            elif name in 'bow_id':
                self.field[name] = QtWidgets.QComboBox(self)
                self.model_bow = self.my_table_model(model.Bow, session)
                self.field[name].setModel(self.model_bow)
            elif name in 'age_id':
                self.field[name] = QtWidgets.QComboBox(self)
                self.model_age = self.my_table_model(model.Age, session)
                self.field[name].setModel(self.model_age)
            else:
                self.field[name] = QtWidgets.QComboBox(self)

            self.gridLayout.addWidget(
                self.field[name], buttonnumber, 2, 1, 1)

        for buttonnumber, label in enumerate(self.labels):
            label.setAutoFillBackground(True)
            self.gridLayout.addWidget(
                label, buttonnumber, 1, 1, 1)
            label.setText(self.tr("{} {}".format(buttonnumber, methods[buttonnumber])))

        self.boxLayout.addLayout(self.gridLayout)
        self.boxLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.close)

    def load_values(self, index, session, table):
        """Values

        :return:
        """
        dataset = session.query(table).get(index)
        for name in self.field:
            if name in self.STRING:
                self.field[name].setText(dataset.__dict__[name])
            elif name in self.INT:
                self.field[name].setValue(dataset.__dict__[name])
            elif name in ('age_id'):
                matches = self.my_match(self.model_age, dataset)
                if matches:
                    self.field[name].setCurrentIndex(matches[0].row())
            elif name in ('bow_id'):
                matches = self.my_match(self.model_bow, dataset)
                if matches:
                    self.field[name].setCurrentIndex(matches[0].row())
            elif name in ('club_id'):
                matches = self.my_match(self.model_club, dataset)
                if matches:
                    self.field[name].setCurrentIndex(matches[0].row())

    def values(self):
        """Values

        :return:
        """
        valve = {}
        for name in self.field:
            if name in self.STRING:
                valve[name] = self.field[name].text()
            elif name in self.INT:
                valve[name] = self.field[name].text()
            elif name in 'age_id':
                ind = self.model_age.index(self.field[name].currentIndex(), 1)
                valve[name] = self.model_age.data(ind, Qt.DisplayRole)
            elif name in 'bow_id':
                ind = self.model_bow.index(self.field[name].currentIndex(), 1)
                valve[name] = self.model_bow.data(ind, Qt.DisplayRole)
            elif name in 'club_id':
                ind = self.model_club.index(self.field[name].currentIndex(), 1)
                valve[name] = self.model_club.data(ind, Qt.DisplayRole)
        return (valve)

    @staticmethod
    def get_values(session, table, model):
        """static method to create the dialog and return
        (dialog.values, accepted)

        :param session: session
        :type session: sqlalchemy session
        :param table: Database actual table
        :type table: table
        :param model: Database model
        :type model: model
        :returns: dialog.values, accepted
        :rtype: dict, bool
        """
        dialog = DlgSqlTable(session, table, model)
        result = dialog.exec_()
        return (dialog.values(), result == QtWidgets.QDialog.Accepted)

    @staticmethod
    def edit_values(session, table, model, idEdit):
        """static method to create the dialog and return
        (dialog.values, accepted)

        :param session: session
        :type session: sqlalchemy session
        :param table: Database actual table
        :type table: table
        :param model: Database model
        :type model: model
        :param idEdit: actual id to edit
        :type idEdit: int
        :returns: dialog.values, accepted
        :rtype: dict, bool
        """
        dialog = DlgSqlTable(session, table, model)
        dialog.load_values(idEdit, session, table)
        result = dialog.exec_()
        return (dialog.values(), result == QtWidgets.QDialog.Accepted)

    @classmethod
    def my_table_model(cls, model, session):
        return SqlAlchemyTableModel(session, model, [
            ('Name', model.name, "name", {"editable": True}),
            ('Id', model.id, "id", {"editable": False})])

    @classmethod
    def my_match(cls, model, dataset):
        return model.match(
            model.index(0, 1), QtCore.Qt.DisplayRole,
            dataset.__dict__[name], 1, QtCore.Qt.MatchExactly)
