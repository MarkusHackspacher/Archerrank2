# -*- coding: utf-8 -*-

"""
Archerank2

Copyright (C) <2019-2024> Markus Hackspacher

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

try:
    from PyQt6.Qt import QModelIndex, Qt
    from PyQt6.QtCore import PYQT_VERSION_STR
except ImportError:
    from PyQt5.Qt import PYQT_VERSION_STR, QModelIndex, Qt

from sqlalchemy import create_engine, orm

from modules import model
from modules.ext.alchemical_model import SqlAlchemyTableModel


class TestSqlAlchemyTableModel(TestCase):
    def setUp(self):
        """Create an engine and create all the tables we need

        @return:
        """
        engine = create_engine('sqlite:///:memory:', echo=False)
        model.Base.metadata.bind = engine
        model.Base.metadata.create_all(engine)

        # Set up the session
        sm = orm.sessionmaker(bind=engine, autoflush=True, autocommit=False,
                              expire_on_commit=True)
        self.session = orm.scoped_session(sm)

        self.model_user = SqlAlchemyTableModel(self.session, model.User, [
            ('Id', model.User.id, "id", {"editable": False, "dnd": False}),
            ('Lastname', model.User.lastname, "lastname", {"editable": True}),
            ('Name', model.User.name, "name", {"editable": True}),
            ('Score', model.User.score, "score", {"editable": True}),
            ('Kill Points', model.User.killpt, "killpt", {"editable": True}),
            ('Club', model.User.club_id, "clubname", {"editable": False}),
            ('Age', model.User.age_id, "agename", {"editable": False}),
            ('Bow', model.User.bow_id, "bowname", {"editable": False})])
        # self.table = QTableView()
        # self.table.setModel(self.model_user)

    def test_headerData(self):
        header = self.model_user.headerData(1, Qt.Orientation.Horizontal, Qt.ItemDataRole.DisplayRole)
        print(dir(header))
        print(type(header))
        # print(header.canView())
        # self.assertEqual(header.data(), QVariant.toPoint())
        # self.assertEqual(header.canConvert().toString(), 'Lastname')

        header = self.model_user.headerData(0, Qt.Orientation.Vertical, Qt.ItemDataRole.DisplayRole)
        # self.assertEqual(header.value.data(), None)

    def test_setFilter(self):
        self.model_user.setFilter(None)

    def test_flags(self):
        index = QModelIndex()
        if int(PYQT_VERSION_STR[0]) >= 6:
            self.assertEqual(self.model_user.flags(index).value, 33)
            self.assertEqual(self.model_user.flags(index).name, 'ItemIsSelectable|ItemIsEnabled')
        else:
            self.assertEqual(self.model_user.flags(index).__int__(), 33)

    def test_supportedDropActions(self):
        self.model_user.supportedDropActions()

    def test_dropMimeData(self):
        self.session.add(model.User(name='John', lastname='Dow'))
        self.model_user.refresh()
        index = self.model_user.createIndex(0, 2)
        if int(PYQT_VERSION_STR[0]) >= 6:
            self.assertEqual(
                self.model_user.dropMimeData('name', Qt.MoveAction, 0, 2, index), None)
        else:
            self.assertEqual(
                self.model_user.dropMimeData('name', Qt.MoveAction, 0, 2, index), False)

        self.assertEqual(
            self.model_user.dropMimeData('a', Qt.DropAction, 0, 2, index), None)
        self.assertEqual(self.model_user.data(index, Qt.ItemDataRole.DisplayRole), 'John')

    def test_rowCount(self):
        self.assertEqual(self.model_user.rowCount(), 0)
        self.session.add(model.User(name='John', lastname='Dow'))
        self.model_user.refresh()
        self.assertEqual(self.model_user.rowCount(), 1)

    def test_columnCount(self):
        self.assertEqual(self.model_user.columnCount(), 8)

    def test_data(self):
        """test data and setData"""
        index = QModelIndex()
        index.sibling(0, 0)
        self.assertEqual(index.isValid(), False)
        self.assertEqual(self.model_user.data(index, Qt.DisplayRole).value(), None)
        self.session.add(model.User(name='John', lastname='Dow'))
        self.model_user.refresh()
        index = self.model_user.createIndex(0, 1)
        self.assertEqual(index.isValid(), True)
        self.assertEqual(self.model_user.data(index, Qt.ItemDataRole.DisplayRole), 'Dow')
        index = self.model_user.createIndex(0, 2)
        self.assertEqual(self.model_user.data(index, Qt.ItemDataRole.DisplayRole), 'John')
        self.assertEqual(self.model_user.setData(index, 'Jonny'), True)
        self.assertEqual(self.model_user.data(index, Qt.ItemDataRole.DisplayRole), 'Jonny')

    def test_refresh(self):
        self.session.add(model.User(name='John', lastname='Dow'))
        self.model_user.refresh()
        self.model_user.sort = (1, 3)
        self.assertEqual(self.model_user.sort, (1, 3))
        self.model_user.refresh()
