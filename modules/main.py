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

import functools
import os
import sys
from os.path import join

from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.Qt import Qt
from PyQt5.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from sqlalchemy import create_engine, orm

from modules import model
from modules.ext.alchemical_model import SqlAlchemyTableModel
from modules.gui.dialogsqltable import DlgSqlTable

importmailmerge = True
try:
    from mailmerge import MailMerge
except ImportError:
    print('Not found docx-mailmerge, no export docx possible')
    importmailmerge = False



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
        self.ui.setWindowIcon(
            QtGui.QIcon(os.path.abspath(os.path.join(
                os.path.dirname(sys.argv[0]), "misc", "archerrank2.svg"))))
        self.initDataBase()
        self.ui.tableView_user.setModel(self.model_user)
        self.ui.tableView_club.setModel(self.model_club)
        self.ui.tableView_age.setModel(self.model_age)
        self.ui.tableView_bow.setModel(self.model_bow)
        self.ui.tableView_user.setColumnHidden(0, True)
        self.ui.tableView_club.setColumnHidden(0, True)
        self.ui.tableView_age.setColumnHidden(0, True)
        self.ui.tableView_bow.setColumnHidden(0, True)
        self.ui.tableView_user.pressed.connect(self.user_selected)
        self.ui.actionPrintPreview.triggered.connect(self.onprint)
        self.ui.actionOverview.triggered.connect(self.onoverview)
        self.ui.actionInfo.triggered.connect(self.oninfo)
        self.ui.actionExit.triggered.connect(self.onexit)
        self.ui.actionCreate_certificates.triggered.connect(self.oncreate)
        user_new = functools.partial(self.entry_new, model.User, self.model_user)
        club_new = functools.partial(self.entry_new, model.Club, self.model_club)
        age_new = functools.partial(self.entry_new, model.Age, self.model_age)
        bow_new = functools.partial(self.entry_new, model.Bow, self.model_bow)
        self.ui.pushButton_user.clicked.connect(user_new)
        self.ui.pushButton_club.clicked.connect(club_new)
        self.ui.pushButton_age.clicked.connect(age_new)
        self.ui.pushButton_bow.clicked.connect(bow_new)
        user_edit = functools.partial(self.entry_edit, model.User, self.model_user)
        club_edit = functools.partial(self.entry_edit, model.Club, self.model_club)
        age_edit = functools.partial(self.entry_edit, model.Age, self.model_age)
        bow_edit = functools.partial(self.entry_edit, model.Bow, self.model_bow)
        self.ui.pushButton_edituser.clicked.connect(user_edit)
        self.ui.pushButton_editclub.clicked.connect(club_edit)
        self.ui.pushButton_editage.clicked.connect(age_edit)
        self.ui.pushButton_editbow.clicked.connect(bow_edit)
        user_del = functools.partial(self.entry_del, model.User, self.model_user)
        club_del = functools.partial(self.entry_del, model.Club, self.model_club)
        age_del = functools.partial(self.entry_del, model.Age, self.model_age)
        bow_del = functools.partial(self.entry_del, model.Bow, self.model_bow)
        self.ui.pushButton_deleteuser.clicked.connect(user_del)
        self.ui.pushButton_deleteclub.clicked.connect(club_del)
        self.ui.pushButton_deleteage.clicked.connect(age_del)
        self.ui.pushButton_deletebow.clicked.connect(bow_del)
        self.ui.actionCreate_certificates.setEnabled(importmailmerge)
        self.ui.show()

    def initDataBase(self):
        filename = False
        while not filename:
            filename = file_dlg('You want load a file or create a new file')
        if 'exit' == filename:
            sys.exit(1)
        # Create an engine and create all the tables we need
        engine = create_engine('sqlite:///{}'.format(filename), echo=False)
        model.base.metadata.bind = engine
        model.base.metadata.create_all(engine)

        # Set up the session
        sm = orm.sessionmaker(bind=engine,
                              autoflush=True,
                              autocommit=False,
                              expire_on_commit=True)
        self.session = orm.scoped_session(sm)


        self.model_user = SqlAlchemyTableModel(self.session, model.User, [
            ('Id', model.User.id, "id", {"editable": False}),
            ('Lastname', model.User.lastname, "lastname", {"editable": True}),
            ('Name', model.User.name, "name", {"editable": True}),
            ('Score', model.User.score, "score", {"editable": True}),
            ('Kill Points', model.User.killpt, "killpt", {"editable": True}),
            ('Club', model.User.club_id, "clubname", {"editable": False}),
            ('Age', model.User.age_id, "agename", {"editable": False}),
            ('Bow', model.User.bow_id, "bowname", {"editable": False})])

        self.model_club = SqlAlchemyTableModel(self.session, model.Club, [
            ('Id', model.Club.id, "id", {"editable": False}),
            ('Name', model.Club.name, "name", {"editable": True, "dnd": True}),
            ('Short', model.Club.short, "short", {"editable": True}),
            ('payment', model.Club.payment, "payment", {"editable": True})])

        self.model_age = SqlAlchemyTableModel(self.session, model.Age, [
            ('Id', model.Age.id, "id", {"editable": False}),
            ('Name', model.Age.name, "name", {"editable": True}),
            ('Short', model.Age.short, "short", {"editable": True}), ])

        self.model_bow = SqlAlchemyTableModel(self.session, model.Bow, [
            ('Id', model.Bow.id, "id", {"editable": False}),
            ('Name', model.Bow.name, "name", {"editable": True}),
            ('Short', model.Bow.short, "short", {"editable": True}), ])


    def entry_new(self, datatable, tablemodel):
        """open dialog for new entry

        datatable could be model.User
        tablemodel could be self.model_user
        """
        newdata = DlgSqlTable.get_values(self.session, datatable, model)
        if newdata[1]:
            self.session.add(datatable(**newdata[0]))
            self.session.commit()
        tablemodel.refresh()

    def select_index(self, tablemodel):
        if tablemodel == self.model_user:
            index = self.ui.tableView_user.currentIndex()
        elif tablemodel == self.model_club:
            index = self.ui.tableView_club.currentIndex()
        elif tablemodel == self.model_age:
            index = self.ui.tableView_age.currentIndex()
        elif tablemodel == self.model_bow:
            index = self.ui.tableView_bow.currentIndex()
        return index

    def entry_edit(self, datatable, tablemodel):
        """open dialog for edit entry

        datatable is model.User
        tablemodel is self.model_user
        """
        index = self.select_index(tablemodel)
        if index.row() < 0:
            QtWidgets.QMessageBox.information(self.ui, self.tr('Info'), self.tr('No line select'))
            return
        ind = tablemodel.index(index.row(), 0)
        newdata = DlgSqlTable.edit_values(self.session, datatable, model,
                                          tablemodel.data(ind, Qt.DisplayRole))
        data = self.session.query(datatable).get(tablemodel.data(ind, Qt.DisplayRole))
        if newdata[1]:
            for key, value in newdata[0].items():
                setattr(data, key, value)
            self.session.commit()
        tablemodel.refresh()

    def entry_del(self, datatable, tablemodel):
        """open dialog for delete entry

        datatable is model.User
        tablemodel is self.model_user
        table_id is club_id
        """
        index = self.select_index(tablemodel)
        if index.row() < 0:
            QtWidgets.QMessageBox.information(self.ui, self.tr('Info'), self.tr('No line select'))
            return
        ind = tablemodel.index(index.row(), 0)
        data = self.session.query(datatable).get(tablemodel.data(ind, Qt.DisplayRole))
        if tablemodel == self.model_user:
            userdata = None
        elif tablemodel == self.model_club:
            userdata = self.session.query(model.User).filter_by(club_id=data.id).first()
        elif tablemodel == self.model_age:
            userdata = self.session.query(model.User).filter_by(age_id=data.id).first()
        elif tablemodel == self.model_bow:
            userdata = self.session.query(model.User).filter_by(bow_id=data.id).first()
        if userdata:
            QtWidgets.QMessageBox.information(
                self.ui, self.tr('Info'),
                self.tr('Cannot delete, reference by {},{}'.format(
                    userdata.name, userdata.lastname)))
            return
        self.session.delete(data)
        self.session.commit()
        tablemodel.refresh()

    def user_selected(self, index):
        """selected user

        :param index:
        :return:
        """
        pass

    def onprint(self):
        """Print Preview"""
        self.editor = QtWidgets.QTextEdit()
        printer = QPrinter(QPrinter.HighResolution)
        previewDialog = QPrintPreviewDialog(printer, self.ui)

        users = self.session.query(model.User).order_by(model.User.bow_id).order_by(
            model.User.age_id).order_by(model.User.score.desc()).order_by(
            model.User.killpt.desc()).order_by(
            model.User.rate.desc()).all()
        names = []
        saveBowAge = ['', '']
        rank = 1
        namesSamePoints = []
        samePoints = [0, 0, 0]
        for userdata in users:
            if (saveBowAge != [userdata.bowname, userdata.agename]):
                names.append('<h2>{}, {}</h2>'.format(
                    userdata.bowname,
                    userdata.agename))
                saveBowAge = [userdata.bowname, userdata.agename]
                rank = 1
                samePoints = [0, 0, 0]
            if samePoints == [userdata.score, userdata.killpt, userdata.rate]:
                namesSamePoints.append('{} {}'.format(userdata.name, userdata.lastname))
                rank -= 1
            names.append('{} {}, {}, {}, {}, {}, {}<br>'.format(
                rank,
                userdata.name,
                userdata.lastname,
                userdata.score,
                userdata.killpt,
                userdata.rate,
                userdata.clubname))
            rank += 1
            samePoints = [userdata.score, userdata.killpt, userdata.rate]
        if namesSamePoints:
            infobox = QtWidgets.QMessageBox()
            infobox.setWindowTitle(self.tr('Info'))
            infobox.setText(self.tr(
                'With same Points.<br>{}'.format("<br>".join(namesSamePoints))))
            infobox.exec_()

        self.editor.setHtml(self.tr(
            '<h1>Overview</h1>Rang Name Score Kill Rate Club<br>{}'.format("".join(names))))
        previewDialog.paintRequested.connect(self.editor.print_)
        previewDialog.exec_()

    def onoverview(self):
        """Set the text for the info message box in html format

        :returns: none
        """
        users = self.session.query(model.User).order_by(model.User.bow_id).order_by(
            model.User.age_id).order_by(model.User.score.desc()).order_by(
            model.User.killpt.desc()).all()
        names = []
        for userdata in users:
            names.append('{}, {}, {}, {} {} {}<br>'.format(
                userdata.name,
                userdata.lastname,
                userdata.score,
                userdata.killpt,
                userdata.bowname,
                userdata.agename))
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

    def oncreate(self):
        with MailMerge('input.docx') as document:
            print(document.get_merge_fields())
            document.merge(Editor='docx Mail Merge',
                           Note='Can be used for merging docx documents')
            document.write('output.docx')

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


def file_dlg(text):
    msgBox = QMessageBox()
    msgBox.setIcon(QMessageBox.Question)
    msgBox.setWindowIcon(
        QtGui.QIcon(os.path.abspath(os.path.join(
            os.path.dirname(sys.argv[0]), "misc", "archerrank2.svg"))))
    msgBox.setText("Question")
    msgBox.setInformativeText(text)
    msgBox.addButton('Load', QMessageBox.AcceptRole)
    msgBox.addButton('New', QMessageBox.AcceptRole)
    msgBox.addButton('Exit', QMessageBox.NoRole)
    reply = msgBox.exec_()
    if reply == 0:
        fileName, _ = QFileDialog.getOpenFileName(
            None, "QFileDialog.getOpenFileName()", "",
            "Acherrang2 Files (*.sqlite)")
        return fileName
    elif reply == 1:
        filedialog = QFileDialog()
        filedialog.setFilter(filedialog.filter() | QtCore.QDir.Hidden)
        filedialog.setDefaultSuffix('sqlite')
        filedialog.setAcceptMode(QFileDialog.AcceptSave)
        filedialog.setNameFilters(["Acherrang2 Files (*.sqlite)"])
        if filedialog.exec_() == QFileDialog.Accepted:
            return filedialog.selectedFiles()[0]
        return
    else:
        return "exit"
