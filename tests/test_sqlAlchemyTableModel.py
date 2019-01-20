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

from PyQt5.Qt import QMetaType, QModelIndex, Qt
from sqlalchemy import create_engine, orm

from modules import model
from modules.ext.alchemical_model import SqlAlchemyTableModel


class TestSqlAlchemyTableModel(TestCase):
    def setUp(self):
        """Create an engine and create all the tables we need

        @return:
        """
        engine = create_engine('sqlite:///:memory:', echo=False)
        model.base.metadata.bind = engine
        model.base.metadata.create_all(engine)

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
        header = self.model_user.headerData(1, Qt.Horizontal, Qt.DisplayRole)
        self.assertEqual(header.type(), QMetaType.QString)
        self.assertEqual(header.canConvert(QMetaType.QString), True)
        self.assertEqual(header.value(), 'Lastname')

        header = self.model_user.headerData(0, Qt.Vertical, Qt.DisplayRole)
        self.assertEqual(header.value(), None)

    def test_setFilter(self):
        self.model_user.setFilter(None)

    def test_flags(self):
        index = QModelIndex()
        print(dir(self.model_user.flags(index)))
        self.assertEqual(self.model_user.flags(index).__int__(), 33)

    def test_supportedDropActions(self):
        self.model_user.supportedDropActions()

    def test_dropMimeData(self):
        self.session.add(model.User(name='John', lastname='Dow'))
        self.model_user.refresh()
        index = self.model_user.createIndex(0, 2)
        self.assertEqual(
            self.model_user.dropMimeData('name', Qt.MoveAction, 0, 2, index), False)
        self.assertEqual(
            self.model_user.dropMimeData('a', Qt.DropAction, 0, 2, index), None)
        self.assertEqual(self.model_user.data(index, Qt.DisplayRole), 'John')

    def test_rowCount(self):
        self.assertEqual(self.model_user.rowCount(1), 0)

    def test_columnCount(self):
        self.assertEqual(self.model_user.columnCount(0), 8)

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
        self.assertEqual(self.model_user.data(index, Qt.DisplayRole), 'Dow')
        index = self.model_user.createIndex(0, 2)
        self.assertEqual(self.model_user.data(index, Qt.DisplayRole), 'John')
        self.assertEqual(self.model_user.setData(index, 'Jonny'), True)
        self.assertEqual(self.model_user.data(index, Qt.DisplayRole), 'Jonny')

    def test_refresh(self):
        self.session.add(model.User(name='John', lastname='Dow'))
        self.model_user.refresh()
        self.model_user.sort = (1, 3)
        self.assertEqual(self.model_user.sort, (1, 3))
        self.model_user.refresh()
