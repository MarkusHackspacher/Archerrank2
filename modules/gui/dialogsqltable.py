# -*- coding: utf-8 -*-

"""
Archerank2

Copyright (C) <2018-2024> Markus Hackspacher

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
import logging
import os
import sys

try:
    from PyQt6 import QtGui, QtWidgets
    from PyQt6.QtCore import Qt, QTimer
except ImportError:
    from PyQt5 import QtGui, QtWidgets
    from PyQt5.QtCore import Qt, QTimer

from modules.ext.alchemical_model import SqlAlchemyTableModel


class DlgSqlTable(QtWidgets.QDialog):
    STRING = ('name', 'short', 'lastname', 'email', 'address')
    INT = ('killpt', 'sorting', 'score', 'rate', 'sep', 'adult', 'payment')
    ADVER = ('advertising')
    TEXT = ('other')
    """
    Dialog generate from sql table
    """
    def __init__(self, session, table, model, parent=None):
        """Initial user interface and slots

        :returns: none
        """
        super(DlgSqlTable, self).__init__(parent)

        self.setModal(True)
        self.buttonBox = QtWidgets.QDialogButtonBox()
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.StandardButton.Ok |
                                          QtWidgets.QDialogButtonBox.StandardButton.Cancel)
        self.boxLayout = QtWidgets.QBoxLayout(
            QtWidgets.QBoxLayout.Direction.TopToBottom, self)
        self.gridLayout = QtWidgets.QGridLayout()
        self.setWindowTitle(table.__tablename__)
        try:
            self.setWindowIcon(
                QtGui.QIcon(os.path.abspath(os.path.join(
                    "misc", "archerrank2.svg"))))
        except FileNotFoundError:
            self.setWindowIcon(
                QtGui.QIcon(os.path.abspath(os.path.join(
                    os.path.dirname(sys.argv[0]), "misc", "archerrank2.svg"))))
        methods = [m.key for m in table.__table__.columns if not len(m.key) == 2]
        if 'rank' in methods:
            methods.remove('rank')
        methodsname = {
            'name': self.tr('Name'),
            'short': self.tr('Short'),
            'lastname': self.tr('Lastname'),
            'email': self.tr('Email'),
            'address': self.tr('Address'),
            'killpt': self.tr('Kill Hits'),
            'sorting': self.tr('Sorting'),
            'score': self.tr('Score'),
            'rate': self.tr('Name'),
            'sep': self.tr('Sep'),
            'adult': self.tr('Adult'),
            'payment': self.tr('Pay for'),
            'advertising': self.tr('Advertising'),
            'other': self.tr('Other'),
            'club_id': self.tr('Club'),
            'bow_id': self.tr('Bow'),
            'age_id': self.tr('Age'),
            }
        self.labels = [QtWidgets.QLabel(self) for _ in methods]
        self.field = {}
        self.model_club = self.my_table_model(model.Club, session)
        self.model_age = self.my_table_model(model.Age, session)
        self.model_bow = self.my_table_model(model.Bow, session)
        for buttonnumber, name in enumerate(methods):
            if name in self.STRING:
                self.field[name] = QtWidgets.QLineEdit(self)
                self.field[name].setToolTip(self.tr(f'Edit {name}'))
            elif name in self.TEXT:
                self.field[name] = QtWidgets.QTextEdit(self)
                self.field[name].setToolTip(self.tr(f'Edit {name}'))
            elif name in self.INT:
                self.field[name] = QtWidgets.QSpinBox(self)
                self.field[name].setToolTip(self.tr(f'Edit {name}'))
            elif name in ('club_id', 'bow_id', 'age_id'):
                self.field[name] = QtWidgets.QComboBox(self)
                self.field[name].setModel(getattr(self, 'model_' + name[:-3]))
                self.field[name].setToolTip(self.tr(f'Select a {name[:-3]}'))
            elif name in self.ADVER:
                self.field[name] = QtWidgets.QComboBox(self)
                self.field[name].addItem(self.tr('Not Set'))
                self.field[name].addItem(self.tr('no advertising, no save address for further use'))
                self.field[name].addItem(self.tr('can save address'))
                self.field[name].addItem(self.tr('by email'))
                self.field[name].addItem(self.tr('by letter'))
                self.field[name].addItem(self.tr('by email and letter'))
                self.field[name].setToolTip(self.tr('Select advertising level'))
                # self.field[name].setItemData(0, self.tr('Tooltip for [0]'), Qt.ToolTipRole)
            else:
                self.field[name] = QtWidgets.QLabel(self)
                logging.debug(f"for {name} no box def")
            self.gridLayout.addWidget(
                self.field[name], buttonnumber, 2, 1, 1)

        for buttonnumber, label in enumerate(self.labels):
            label.setAutoFillBackground(True)
            self.gridLayout.addWidget(
                label, buttonnumber, 1, 1, 1)
            label.setText(self.tr(f"{buttonnumber} {methodsname[methods[buttonnumber]]}"))

        self.members = QtWidgets.QTextEdit(self)
        self.gridLayout.addWidget(self.members,  buttonnumber+1, 1, 1, 2)
        self.boxLayout.addLayout(self.gridLayout)
        self.boxLayout.addWidget(self.buttonBox)

        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.close)

    def load_values(self, index, session, table):
        """Values

        :return:
        """
        dataset = session.query(table).filter_by(id=index).first()
        if not table.__tablename__ == "users":
            self.members.setText(self.tr(f"{len(dataset.members)} members:"))
            for members in dataset.members:
                self.members.append(self.tr(
                    f"Name: {members.name} {members.lastname}"))
        for name in self.field:
            if name in self.STRING or name in self.TEXT:
                self.field[name].setText(dataset.__dict__[name])
            elif name in self.INT:
                self.field[name].setValue(dataset.__dict__[name])
            elif name in ('age_id', 'bow_id', 'club_id'):
                logging.debug(f'''Show {name} index {dataset.__dict__[name]}
                              from user {dataset.__dict__['name']}''')
                matches = self.matchIndex(getattr(
                    self, 'model_' + name[:-3]), dataset.__dict__[name])
                if matches:
                    self.field[name].setCurrentIndex(matches[0].row())
            elif name in self.ADVER:
                self.field[name].setCurrentIndex(dataset.__dict__[name])

    def values(self):
        """Values

        :return:
        """
        valve = {}
        for name in self.field:
            if name in self.STRING:
                valve[name] = self.field[name].text()
            elif name in self.TEXT:
                valve[name] = self.field[name].toPlainText()
            elif name in self.INT:
                valve[name] = self.field[name].text()
            elif name in 'age_id':
                ind = self.model_age.index(self.field[name].currentIndex(), 1)
                valve[name] = self.model_age.data(ind, Qt.ItemDataRole.DisplayRole)
            elif name in 'bow_id':
                ind = self.model_bow.index(self.field[name].currentIndex(), 1)
                valve[name] = self.model_bow.data(ind, Qt.ItemDataRole.DisplayRole)
            elif name in 'club_id':
                ind = self.model_club.index(self.field[name].currentIndex(), 1)
                valve[name] = self.model_club.data(ind, Qt.ItemDataRole.DisplayRole)
            elif name in self.ADVER:
                valve[name] = self.field[name].currentIndex()
        return valve

    @staticmethod
    def get_values(session, table, model, test=None, parent=None):
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
        dialog = DlgSqlTable(session, table, model, parent)
        if test:
            QTimer.singleShot(500, dialog.accept)
        result = dialog.exec()
        return dialog.values(), result == QtWidgets.QDialog.DialogCode.Accepted

    @staticmethod
    def edit_values(session, table, model, idEdit, test=None, parent=None):
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
        dialog = DlgSqlTable(session, table, model, parent)
        dialog.load_values(idEdit, session, table)
        if test:
            QTimer.singleShot(500, dialog.accept)
        result = dialog.exec()
        return dialog.values(), result == QtWidgets.QDialog.DialogCode.Accepted

    @classmethod
    def my_table_model(cls, model, session):
        return SqlAlchemyTableModel(session, model, [
            ('Name', model.name, "name", {"editable": True}),
            ('Id', model.id, "id", {"editable": False})])

    @classmethod
    def matchIndex(cls, model, index):
        return model.match(
            model.index(0, 1), Qt.ItemDataRole.DisplayRole,
            index, 1, Qt.MatchFlag.MatchExactly)
