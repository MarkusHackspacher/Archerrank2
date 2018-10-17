#!/usr/bin/env python3
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

from PyQt5 import QtGui, QtCore, QtWidgets, uic

from sqlalchemy import orm, literal,  create_engine


from alchemical_model import SqlAlchemyTableModel

sys.path.append('..')

from modules import model


# Create an engine and create all the tables we need
engine = create_engine('sqlite:///../test1.sqlite', echo=False)
model.base.metadata.bind = engine
model.base.metadata.create_all(engine)

# Set up the session
sm = orm.sessionmaker(bind=engine,
                      autoflush=True,
                      autocommit=True,
                      expire_on_commit=True)
session = orm.scoped_session(sm)

tablemodel = SqlAlchemyTableModel(session, model.Club, 3)


class DlgClub(QtWidgets.QDialog):
    """
    Club Overview Dialog
    """
    def __init__(self):
        """init Dialog
        """
        QtWidgets.QDialog.__init__(self)
        self.ui = uic.loadUi(os.path.abspath(os.path.join(
            os.path.dirname(sys.argv[0]),
            "..", "modules", "gui", "club.ui")))


def window():
    app = QtWidgets.QApplication(sys.argv)
    w = QtWidgets.QWidget()
    b = QtWidgets.QPushButton(w)
    b.setText("Hello World!")
    b.move(50, 50)
    b.clicked.connect(new_club)
    w.setWindowTitle("PyQt Dialog demo")
    w.show()
    sys.exit(app.exec_())

def new_club():
    """insert a new user

    :return:
    """
    dlg = DlgClub()
    dlg.exec_()

if __name__ == '__main__':
    window()

