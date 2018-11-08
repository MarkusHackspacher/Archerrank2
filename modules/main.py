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

import sys
import os
from os.path import join

from PyQt5 import QtGui, QtCore, QtWidgets, uic
from PyQt5.Qt import Qt

from sqlalchemy import orm, literal,  create_engine


from modules.ext.alchemical_model import SqlAlchemyTableModel
from modules.gui.dialogsqltable import DlgSqlTable

sys.path.append('..')

from modules import model


# Create an engine and create all the tables we need
engine = create_engine('sqlite:///test2.sqlite', echo=False)
model.base.metadata.bind = engine
model.base.metadata.create_all(engine)

# Set up the session
sm = orm.sessionmaker(bind=engine,
                      autoflush=True,
                      autocommit=False,
                      expire_on_commit=True)
session = orm.scoped_session(sm)

if not session.query(model.Club).all():
    session.add(model.Club(name='VfB Stuttgart', short='VfB'))
if not session.query(model.Age).all():
    session.add(model.Age(name='Beginner', short='start'))
    session.add(model.Age(name='Best of All', short='Elite'))
    session.add(model.Age(name='Kid', short='Kid', id=23))
if not session.query(model.Bow).all():
    session.add(model.Bow(name='Longbow', short='LB'))
if not session.query(model.User).all():
    session.add(model.User(name='John', lastname='Dow', club_id=1, age_id=1, bow_id=1))

model_user = SqlAlchemyTableModel(session, model.User, [('Id', model.User.id, "id", {"editable": False}),
                                                        ('Lastname', model.User.lastname, "lastname", {"editable": True}),
                                                        ('Name', model.User.name, "name", {"editable": True}),
                                                        ('Score', model.User.score, "score", {"editable": True}),
                                                        ('Kill Points', model.User.killpt, "killpt", {"editable": True}),
                                                        ('Club', model.User.club_id, "clubname", {"editable": False}),
                                                        ('Age', model.User.age_id, "agename", {"editable": False}),
                                                        ('Bow', model.User.bow_id, "bowname", {"editable": False})])

model_club = SqlAlchemyTableModel(session, model.Club, [('Id', model.Club.id, "id", {"editable": False}),
                                                        ('Name', model.Club.name, "name", {"editable": True, "dnd": True}),
                                                        ('Short', model.Club.short, "short", {"editable": True}),
                                                        ('payment', model.Club.payment, "payment", {"editable": True})])

model_age = SqlAlchemyTableModel(session, model.Age, [('Id', model.Age.id, "id", {"editable": False}),
                                                      ('Name', model.Age.name, "name", {"editable": True}),
                                                      ('Short', model.Age.short, "short", {"editable": True}), ])

model_bow = SqlAlchemyTableModel(session, model.Bow, [('Id', model.Bow.id, "id", {"editable": False}),
                                                      ('Name', model.Bow.name, "name", {"editable": True}),
                                                      ('Short', model.Bow.short, "short", {"editable": True}), ])


class Main(QtCore.QObject):
    """The GUI and program of the pyLottoSimu.
    """
    def __init__(self, arguments):
        """Initial user interface and slots

        :returns: none
        """
        super(Main, self).__init__()
        self.app = QtWidgets.QApplication([])
        if len(arguments) > 1:
            locale = arguments[1]
        else:
            locale = str(QtCore.QLocale.system().name())
            print("locale: " + locale)
        translator = QtCore.QTranslator(self.app)
        translator.load(join("modules", "pyfbm_" + locale))
        self.app.installTranslator(translator)


        # Set up the user interface from Designer.
        self.ui = uic.loadUi(os.path.abspath(os.path.join(
            os.path.dirname(sys.argv[0]),
            "modules", "gui", "main.ui")))
        #self.ui.setWindowIcon(
        #    QtGui.QIcon(os.path.abspath(os.path.join(
        #        os.path.dirname(sys.argv[0]), "misc", "archerrank2.svg"))))

        self.ui.tableView_user.setModel(model_user)
        self.ui.tableView_club.setModel(model_club)
        self.ui.tableView_age.setModel(model_age)
        self.ui.tableView_bow.setModel(model_bow)
        self.ui.tableView_user.setColumnHidden(0, True)
        self.ui.tableView_club.setColumnHidden(0, True)
        self.ui.tableView_age.setColumnHidden(0, True)
        self.ui.tableView_bow.setColumnHidden(0, True)
        self.ui.tableView_user.pressed.connect(self.user_selected)
        self.ui.actionExit.triggered.connect(self.onexit)
        self.ui.pushButton_user.clicked.connect(self.user_new)
        self.ui.pushButton_club.clicked.connect(self.club_new)
        self.ui.pushButton_age.clicked.connect(self.age_new)
        self.ui.pushButton_bow.clicked.connect(self.bow_new)
        self.ui.pushButton_edituser.clicked.connect(self.user_edit)
        self.ui.pushButton_deleteuser.clicked.connect(self.user_del)
        self.ui.pushButton_editclub.clicked.connect(self.club_edit)
        self.ui.pushButton_deleteclub.clicked.connect(self.club_del)
        self.ui.pushButton_editage.clicked.connect(self.age_edit)
        self.ui.pushButton_deleteage.clicked.connect(self.age_del)
        self.ui.pushButton_editbow.clicked.connect(self.bow_edit)
        self.ui.pushButton_deletebow.clicked.connect(self.bow_del)
        self.ui.show()

    def user_new(self):
        """open dialog for new user
        """
        newdata = DlgSqlTable.get_values(session, model.User, model)
        if newdata[1]:
            session.add(model.User(**newdata[0]))
            session.commit()
        model_user.refresh()

    def club_new(self):
        """open dialog for new club
        """
        newdata = DlgSqlTable.get_values(session, model.Club, model)
        if newdata[1]:
            session.add(model.Club(**newdata[0]))
            session.commit()
        model_club.refresh()

    def age_new(self):
        """open dialog for new age
        """
        newdata = DlgSqlTable.get_values(session, model.Age, model)
        if newdata[1]:
            session.add(model.Age(**newdata[0]))
            session.commit()
        model_age.refresh()

    def bow_new(self):
        """open dialog for new bow
        """
        newdata = DlgSqlTable.get_values(session, model.Bow, model)
        if newdata[1]:
            session.add(model.Bow(**newdata[0]))
            session.commit()
        model_bow.refresh()

    def user_edit(self):
        """open dialog for edit user
        """
        index = self.ui.tableView_user.currentIndex()
        if index.row() < 0:
            return
        ind = model_user.index(index.row(), 0)
        newdata = DlgSqlTable.edit_values(session, model.User, model, model_user.data(ind, Qt.DisplayRole))
        data = session.query(model.User).get(model_user.data(ind, Qt.DisplayRole))
        if newdata[1]:
            for key, value in newdata[0].items():
                setattr(data, key, value)
            session.commit()
        model_user.refresh()

    def club_edit(self):
        """open dialog for edit club
        """
        index = self.ui.tableView_club.currentIndex()
        if index.row() < 0:
            return
        ind = model_club.index(index.row(), 0)
        newdata = DlgSqlTable.edit_values(session, model.Club, model, model_club.data(ind, Qt.DisplayRole))
        data = session.query(model.Club).get(model_club.data(ind, Qt.DisplayRole))
        if newdata[1]:
            for key, value in newdata[0].items():
                setattr(data, key, value)
            session.commit()
        model_club.refresh()

    def age_edit(self):
        """open dialog for edit age
        """
        index = self.ui.tableView_age.currentIndex()
        if index.row() < 0:
            return
        ind = model_age.index(index.row(), 0)
        newdata = DlgSqlTable.edit_values(session, model.Age, model, model_age.data(ind, Qt.DisplayRole))
        data = session.query(model.Age).get(model_age.data(ind, Qt.DisplayRole))
        if newdata[1]:
            for key, value in newdata[0].items():
                setattr(data, key, value)
            session.commit()
        model_age.refresh()

    def bow_edit(self):
        """open dialog for edit bow
        """
        index = self.ui.tableView_bow.currentIndex()
        if index.row() < 0:
            return
        ind = model_bow.index(index.row(), 0)
        newdata = DlgSqlTable.edit_values(session, model.bow, model, model_bow.data(ind, Qt.DisplayRole))
        data = session.query(model.Bow).get(model_bow.data(ind, Qt.DisplayRole))
        if newdata[1]:
            for key, value in newdata[0].items():
                setattr(data, key, value)
            session.commit()
        model_bow.refresh()

    def user_del(self):
        """open dialog for delete user
        """
        index = self.ui.tableView_user.currentIndex()
        if index.row() < 0:
            return
        model_user.refresh()
        
    def club_del(self):
        """open dialog for delete club
        """
        index = self.ui.tableView_club.currentIndex()
        if index.row() < 0:
            return
        model_club.refresh()
        
    def age_del(self):
        """open dialog for delete age
        """
        index = self.ui.tableView_age.currentIndex()
        if index.row() < 0:
            return
        model_age.refresh()
        
    def bow_del(self):
        """open dialog for delete bow
        """
        index = self.ui.tableView_bow.currentIndex()
        if index.row() < 0:
            return
        model_bow.refresh()
        
    def user_selected(self, index):
        """selected user

        :param index:
        :return:
        """
        print(index.row(), index.column())

    def onexit(self):
        """exit and close

        :return:
        """
        self.ui.close()

    def main_loop(self):
        """application start

        :return:
        """
        self.app.exec_()
