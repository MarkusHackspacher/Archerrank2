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

from sqlalchemy import orm, literal,  create_engine


from modules.ext.alchemical_model import SqlAlchemyTableModel

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

if not session.query(model.User).all():
    session.add(model.User(name='John', lastname='Dow'))
if not session.query(model.Club).all():
    session.add(model.Club(name='VfB Stuttgart', short='VfB'))
if not session.query(model.Age).all():
    session.add(model.Age(name='Best of All', short='Elite'))
if not session.query(model.Bow).all():
    session.add(model.Bow(name='Longbow', short='LB'))

model_user = SqlAlchemyTableModel(session, model.User, [('Name', model.User.name, "name", {"editable": True}),
                                                        ('Lastname', model.User.lastname, "lastname", {"editable": True}),
                                                        ('Club', model.User.club_id, "club_id", {"editable": True}),
                                                        ('Age', model.User.age_id, "age_id", {"editable": True}),
                                                        ('Bow', model.User.bow_id, "bow_id", {"editable": True})])

model_club = SqlAlchemyTableModel(session, model.Club, [('Name', model.Club.name, "name", {"editable": True, "dnd": True}),
                                                        ('Short', model.Club.short, "short", {"editable": True}),
                                                        ('payment', model.Club.payment, "payment", {"editable": True})])

model_age = SqlAlchemyTableModel(session, model.Age, [('Name', model.Age.name, "name", {"editable": True}),
                                                        ('Short', model.Age.short, "short", {"editable": True}), ])

model_bow = SqlAlchemyTableModel(session, model.Bow, [('Name', model.Bow.name, "name", {"editable": True}),
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

        self.ui.show()

    def main_loop(self):
        """application start

        :return:
        """
        self.app.exec_()