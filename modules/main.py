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

import functools
import sys
import os
from os.path import join

from PyQt5 import QtGui, QtCore, QtWidgets, uic
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog, QPrintPreviewDialog
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
        self.ui.actionPrintPreview.triggered.connect(self.onprint)
        self.ui.actionOverview.triggered.connect(self.onoverview)
        self.ui.actionInfo.triggered.connect(self.oninfo)
        self.ui.actionExit.triggered.connect(self.onexit)
        user_new = functools.partial(self.entry_new, model.User, model_user)
        club_new = functools.partial(self.entry_new, model.Club, model_club)
        age_new = functools.partial(self.entry_new, model.Age, model_age)
        bow_new = functools.partial(self.entry_new, model.Bow, model_bow)
        self.ui.pushButton_user.clicked.connect(user_new)
        self.ui.pushButton_club.clicked.connect(club_new)
        self.ui.pushButton_age.clicked.connect(age_new)
        self.ui.pushButton_bow.clicked.connect(bow_new)
        user_edit = functools.partial(self.entry_edit, model.User, model_user)
        club_edit = functools.partial(self.entry_edit, model.Club, model_club)
        age_edit = functools.partial(self.entry_edit, model.Age, model_age)
        bow_edit = functools.partial(self.entry_edit, model.Bow, model_bow)
        self.ui.pushButton_edituser.clicked.connect(user_edit)
        self.ui.pushButton_editclub.clicked.connect(club_edit)
        self.ui.pushButton_editage.clicked.connect(age_edit)
        self.ui.pushButton_editbow.clicked.connect(bow_edit)
        user_del = functools.partial(self.entry_del, model.User, model_user)
        club_del = functools.partial(self.entry_del, model.Club, model_club)
        age_del = functools.partial(self.entry_del, model.Age, model_age)
        bow_del = functools.partial(self.entry_del, model.Bow, model_bow)
        self.ui.pushButton_deleteuser.clicked.connect(user_del)
        self.ui.pushButton_deleteclub.clicked.connect(club_del)
        self.ui.pushButton_deleteage.clicked.connect(age_del)
        self.ui.pushButton_deletebow.clicked.connect(bow_del)
        self.ui.show()

    def entry_new(self, datatable, tablemodel):
        """open dialog for new entry

        datatable is model.User
        tablemodel is model_user
        """
        newdata = DlgSqlTable.get_values(session, datatable, model)
        if newdata[1]:
            session.add(datatable(**newdata[0]))
            session.commit()
        tablemodel.refresh()

    def select_index(self, tablemodel):
        if tablemodel == model_user:
            index = self.ui.tableView_user.currentIndex()
        elif tablemodel == model_club:
            index = self.ui.tableView_club.currentIndex()
        elif tablemodel == model_age:
            index = self.ui.tableView_age.currentIndex()
        elif tablemodel == model_bow:
            index = self.ui.tableView_bow.currentIndex()
        return index

    def entry_edit(self, datatable, tablemodel):
        """open dialog for edit entry

        datatable is model.User
        tablemodel is model_user
        """
        index = self.select_index(tablemodel)
        if index.row() < 0:
            QtWidgets.QMessageBox.information(self.ui, 'Info', 'No line select')
            return
        ind = tablemodel.index(index.row(), 0)
        newdata = DlgSqlTable.edit_values(session, datatable, model, tablemodel.data(ind, Qt.DisplayRole))
        data = session.query(datatable).get(tablemodel.data(ind, Qt.DisplayRole))
        if newdata[1]:
            for key, value in newdata[0].items():
                setattr(data, key, value)
            session.commit()
        tablemodel.refresh()

    def entry_del(self, datatable, tablemodel):
        """open dialog for delete entry

        datatable is model.User
        tablemodel is model_user
        table_id is club_id
        """
        index = self.select_index(tablemodel)
        if index.row() < 0:
            QtWidgets.QMessageBox.information(self.ui, 'Info', 'No line select')
            return
        ind = tablemodel.index(index.row(), 0)
        data = session.query(datatable).get(tablemodel.data(ind, Qt.DisplayRole))
        if tablemodel == model_user:
            userdata = None
        elif tablemodel == model_club:
            userdata = session.query(model.User).filter_by(club_id=data.id).first()
        elif tablemodel == model_age:
            userdata = session.query(model.User).filter_by(age_id=data.id).first()
        elif tablemodel == model_bow:
            userdata = session.query(model.User).filter_by(bow_id=data.id).first()
        if userdata:
            QtWidgets.QMessageBox.information(self.ui, 'Info',
                'Cannot delete, reference by {},{}'.format(userdata.name, userdata.lastname))
            return
        session.delete(data)
        session.commit()
        tablemodel.refresh()
        
    def user_selected(self, index):
        """selected user

        :param index:
        :return:
        """
        print(index.row(), index.column())

    def onprint(self):
        """Print Preview"""
        self.editor = QtWidgets.QTextEdit()
        printer = QPrinter(QPrinter.HighResolution)
        previewDialog = QPrintPreviewDialog(printer, self.ui)

        users = session.query(model.User).order_by(model.User.bow_id).order_by(
            model.User.age_id).order_by(model.User.score.desc()).order_by(
            model.User.killpt.desc()).all()
        names = []
        for userdata in users:
            names.append('{}, {}, {}, {} {} {}<br>'.format(
                userdata.name, userdata.lastname, userdata.score, userdata.killpt, userdata.bowname, userdata.agename))
        self.editor.setHtml('<h1>Headline</h1>{}'.format("".join(names)))
        self.editor.append('{}'.format("".join(names)))
        previewDialog.paintRequested.connect(self.editor.print_)
        previewDialog.exec_()



    def onoverview(self):
        """Set the text for the info message box in html format

        :returns: none
        """
        users = session.query(model.User).order_by(model.User.bow_id).order_by(
            model.User.age_id).order_by(model.User.score.desc()).order_by(
            model.User.killpt.desc()).all()
        names = []
        for userdata in users:
            names.append('{}, {}, {}, {} {} {}<br>'.format(
                userdata.name, userdata.lastname, userdata.score, userdata.killpt, userdata.bowname, userdata.agename))
        infobox = QtWidgets.QMessageBox()
        infobox.setWindowTitle(self.tr('Info'))

        infobox.setText(self.tr(
            'Overview.<br>{}'.format("".join(names))))
        infobox.exec_()

    def oninfo(self):
        """Set the text for the info message box in html format

        :returns: none
        """
        infobox = QtWidgets.QMessageBox()
        infobox.setWindowTitle(self.tr('Info'))
        infobox.setText(self.tr(
            'Archerrank2. A tool for the evaluation of archery tournaments.<br>'
            'Archerrank2 is free software and use GNU General Public License '
            '<a href="http://www.gnu.org/licenses/">www.gnu.org/licenses</a>'))
        infobox.setInformativeText(self.tr(
            'More Information about the program at '
            '<a href="https://github.com/MarkusHackspacher/Archerrank2">'
            'github.com/MarkusHackspacher/Archerrank2</a>'))
        infobox.exec_()

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
