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

import functools
import logging
import sys
from os.path import abspath, dirname, join

try:
    from PyQt6 import QtGui, QtWidgets
    from PyQt6.QtCore import (PYQT_VERSION_STR, QDir, QLocale, QObject, Qt,
                              QTimer, QTranslator)
    from PyQt6.QtWidgets import (QDockWidget, QFileDialog, QMessageBox,
                                 QPushButton, QTableView, QVBoxLayout, QWidget)
    LeftDockWidgetArea = Qt.DockWidgetArea.LeftDockWidgetArea
    RightDockWidgetArea = Qt.DockWidgetArea.RightDockWidgetArea
except ImportError as err:
    from PyQt5 import QtGui, QtWidgets
    from PyQt5.Qt import PYQT_VERSION_STR
    from PyQt5.QtCore import QDir, QLocale, QObject, Qt, QTimer, QTranslator
    from PyQt5.QtWidgets import (QDockWidget, QFileDialog, QMessageBox,
                                 QPushButton, QTableView, QVBoxLayout, QWidget)
    LeftDockWidgetArea, RightDockWidgetArea = Qt.LeftDockWidgetArea, Qt.RightDockWidgetArea
    print(f"main.py: ImportError {err=}, {type(err)=}")
except Exception as err:
    print(f"main.py: Unexpected {err=}, {type(err)=}")
    raise

from sqlalchemy import create_engine, orm

from modules import VERSION_STR, model, writexlsx
from modules.ext.alchemical_model import SqlAlchemyTableModel
from modules.gui.dialogsqltable import DlgSqlTable
from modules.gui.mainwindow import Ui_MainWindow
from modules.gui.printdialog import DlgPrint

import_mailmerge = True
try:
    from mailmerge import MailMerge
except ImportError:
    print('Not found docx-mailmerge, no export docx possible')
    import_mailmerge = False
logger = logging.getLogger(__name__)


class Main(QtWidgets.QApplication):
    """The GUI and program of the Archerank2.
    """

    def __init__(self, arguments):
        """Initial user interface and slots

        :returns: none
        """
        super(Main, self).__init__(sys.argv)
        print(arguments.log * 10)
        logging.basicConfig(format='%(levelname)s:%(message)s', level=arguments.log * 10)
        logging.info(f'Python Version: {sys.version_info.major}.{sys.version_info.minor}')
        logging.info(f'PyQt Version: {PYQT_VERSION_STR}')
        logging.info(f'Archerrank2 Version: {VERSION_STR}')
        if arguments.language:
            locale = arguments.language
        else:
            locale = str(QLocale.system().name())
        logging.info(f'locale: {locale}')
        translator = QTranslator(self)
        translator.load(join("po", "archerrank_" + locale))
        self.installTranslator(translator)
        self.initDataBase(arguments.database)
        self.dialog = ArcherrankDialog(self)

    def initDataBase(self, filename=None):
        while not filename:
            filename = self.file_dlg(self.tr('You want load a file or create a new file'))
        if 'exit' == filename:
            sys.exit(1)
        # Create an engine and create all the tables we need
        logging.info(f'database: {filename}')
        engine = create_engine('sqlite:///{}'.format(filename), echo=False)
        model.Base.metadata.bind = engine
        model.Base.metadata.create_all(engine)

        # Set up the session
        sm = orm.sessionmaker(bind=engine,
                              autoflush=True,
                              autocommit=False,
                              expire_on_commit=True)
        self.session = orm.scoped_session(sm)

        self.model_user = SqlAlchemyTableModel(self.session, model.User, [
            ('Id', model.User.id, "id", {"editable": False}),
            (self.tr('Lastname'), model.User.lastname, "lastname", {"editable": True}),
            (self.tr('Name'), model.User.name, "name", {"editable": True}),
            (self.tr('Score'), model.User.score, "score", {"editable": True}),
            (self.tr('Kill Points'), model.User.killpt, "killpt", {"editable": True}),
            (self.tr('Club'), model.User.club_id, "clubname", {"editable": False}),
            (self.tr('Age'), model.User.age_id, "agename", {"editable": False}),
            (self.tr('Bow'), model.User.bow_id, "bowname", {"editable": False})], self)

        self.model_club = SqlAlchemyTableModel(self.session, model.Club, [
            ('Id', model.Club.id, "id", {"editable": False}),
            (self.tr('Name'), model.Club.name, "name", {"editable": True, "dnd": True}),
            (self.tr('Short'), model.Club.short, "short", {"editable": True}),
            (self.tr('payment'), model.Club.payment, "payment", {"editable": True}),
            (self.tr('members'), model.Club.membersCount, "membersCount", {"editable": False}),
            (self.tr('address'), model.Club.address, "address", {"editable": True})], self)

        self.model_age = SqlAlchemyTableModel(self.session, model.Age, [
            ('Id', model.Age.id, "id", {"editable": False}),
            (self.tr('Name'), model.Age.name, "name", {"editable": True}),
            (self.tr('Short'), model.Age.short, "short", {"editable": True}),
            (self.tr('members'), model.Club.membersCount, "membersCount", {"editable": False}), ], self)

        self.model_bow = SqlAlchemyTableModel(self.session, model.Bow, [
            ('Id', model.Bow.id, "id", {"editable": False}),
            (self.tr('Name'), model.Bow.name, "name", {"editable": True}),
            (self.tr('Short'), model.Bow.short, "short", {"editable": True}),
            (self.tr('members'), model.Club.membersCount, "membersCount", {"editable": False}), ], self)

    def file_dlg(self, text):
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Icon.Question)
        try:
            msg_box.setWindowIcon(
                QtGui.QIcon(join(
                    "misc", "archerrank2.svg")))
        except FileNotFoundError:
            msg_box.setWindowIcon(
                QtGui.QIcon(abspath(join(
                    dirname(sys.argv[0]), "misc", "archerrank2.svg"))))
        msg_box.setText(self.tr("Question"))
        msg_box.setInformativeText(text)
        open_button = msg_box.addButton(self.tr('Open'), QMessageBox.ButtonRole.AcceptRole)
        new_button = msg_box.addButton(self.tr('New'), QMessageBox.ButtonRole.AcceptRole)
        msg_box.addButton(self.tr('Exit'), QMessageBox.ButtonRole.NoRole)
        msg_box.exec()
        if msg_box.clickedButton() == open_button:
            fileName, _ = QFileDialog.getOpenFileName(
                None, "QFileDialog.getOpenFileName()", "",
                "Acherrang2 Files (*.sqlite)")
            return fileName
        elif msg_box.clickedButton() == new_button:
            filedialog = QFileDialog(msg_box)
            filedialog.setFilter(filedialog.filter() | QDir.Filter.Hidden)
            filedialog.setFileMode(QFileDialog.FileMode.AnyFile)
            filedialog.setDefaultSuffix('sqlite')
            filedialog.setNameFilters(["Acherrang2 Files (*.sqlite)"])
            if filedialog.exec():
                return filedialog.selectedFiles()[0]
            return
        else:
            return "exit"

    def main_loop(self):
        """application start

        :return:
        """
        self.exec()


class ArcherrankDialog(QObject):
    """The GUI of the Archerrank.
    """
    def __init__(self, main):
        """Initial user interface and slots

        :returns: none
        """
        QObject.__init__(self)
        self.exportDir = False
        self.main = main
        # Set up the user interface from Designer.
        """
        try:
            self.ui = uic.loadUi(abspath(join(
                os.path.dirname(sys.argv[0]),
                "modules", "gui", "main.ui")))
        except FileNotFoundError:
            self.ui = uic.loadUi(join(
                "modules", "gui", "main.ui"))
        """
        self.ui = Ui_MainWindow()
        try:
            self.ui.setWindowIcon(
                QtGui.QIcon(abspath(join(
                    "misc", "archerrank2.svg"))))
        except FileNotFoundError:
            self.ui.setWindowIcon(
                QtGui.QIcon(abspath(join(
                    dirname(sys.argv[0]), "misc", "archerrank2.svg"))))
        self.createDockWindows()
        self.ui.tableView_user.setModel(self.main.model_user)
        self.ui.tableView_club.setModel(self.main.model_club)
        self.ui.tableView_age.setModel(self.main.model_age)
        self.ui.tableView_bow.setModel(self.main.model_bow)
        self.ui.tableView_user.setColumnHidden(0, True)
        self.ui.tableView_club.setColumnHidden(0, True)
        self.ui.tableView_age.setColumnHidden(0, True)
        self.ui.tableView_bow.setColumnHidden(0, True)
        self.ui.tableView_user.pressed.connect(self.user_selected)
        self.ui.actionPrintPreview.triggered.connect(self.onprint)
        self.ui.actionOverview.triggered.connect(self.on_overview)
        self.ui.actionInfo.triggered.connect(self.oninfo)
        self.ui.actionExit.triggered.connect(self.on_exit)
        self.ui.actionCreateCertificates.triggered.connect(self.on_create_winner)
        self.ui.actionCreateAddress.triggered.connect(self.on_create_adress)
        self.ui.actionXLSX_Export.triggered.connect(self.on_xlsx_export)
        self.ui.actionCreateCertificates.setEnabled(import_mailmerge)
        self.ui.actionCreateAddress.setEnabled(import_mailmerge)
        self.ui.actionXLSX_Export.setEnabled(writexlsx.import_openpyxl)
        self.ui.show()

    def entry_new(self, datatable, tablemodel, test=None):
        """open dialog for new entry

        datatable could be model.User
        tablemodel could be self.model_user
        """
        if datatable == model.User:
            if not self.main.session.query(model.Club).first():
                QtWidgets.QMessageBox.information(self.ui, self.tr('Info'), self.tr(
                    'Add first Club'))
                return
            if not self.main.session.query(model.Age).first():
                QtWidgets.QMessageBox.information(self.ui, self.tr('Info'), self.tr(
                    'Add first Age'))
                return
            if not self.main.session.query(model.Bow).first():
                QtWidgets.QMessageBox.information(self.ui, self.tr('Info'), self.tr(
                    'Add first Bow'))
                return
        newdata = DlgSqlTable.get_values(self.main.session, datatable, model, test, parent=self.ui)
        if newdata[1]:
            self.main.session.add(datatable(**newdata[0]))
            self.main.session.commit()
        tablemodel.refresh()

    def select_index(self, tablemodel):
        if tablemodel == self.main.model_user:
            index = self.ui.tableView_user.currentIndex()
        elif tablemodel == self.main.model_club:
            index = self.ui.tableView_club.currentIndex()
        elif tablemodel == self.main.model_age:
            index = self.ui.tableView_age.currentIndex()
        elif tablemodel == self.main.model_bow:
            index = self.ui.tableView_bow.currentIndex()
        return index

    def entry_edit(self, datatable, tablemodel, test=None):
        """open dialog for edit entry

        datatable is model.User
        tablemodel is self.model_user
        """
        index = self.select_index(tablemodel)
        if index.row() < 0:
            QtWidgets.QMessageBox(self.ui).information(
                self.ui, self.tr('Info'), self.tr('No line select'))
            return
        ind = tablemodel.index(index.row(), 0)
        newdata = DlgSqlTable.edit_values(self.main.session, datatable, model,
                                          tablemodel.data(ind, Qt.ItemDataRole.DisplayRole),
                                          test, parent=self.ui)
        data = self.main.session.query(datatable).filter_by(
            id=tablemodel.data(ind, Qt.ItemDataRole.DisplayRole)).first()
        if newdata[1]:
            for key, value in newdata[0].items():
                setattr(data, key, value)
            self.main.session.commit()
        tablemodel.refresh()

    def entry_delete(self, datatable, tablemodel):
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
        data = self.main.session.query(datatable).filter_by(
            id=tablemodel.data(ind, Qt.ItemDataRole.DisplayRole)).first()
        if tablemodel == self.main.model_user:
            userdata = None
        elif tablemodel == self.main.model_club:
            userdata = self.main.session.query(model.User).filter_by(club_id=data.id).first()
        elif tablemodel == self.main.model_age:
            userdata = self.main.session.query(model.User).filter_by(age_id=data.id).first()
        elif tablemodel == self.main.model_bow:
            userdata = self.main.session.query(model.User).filter_by(bow_id=data.id).first()
        if userdata:
            QtWidgets.QMessageBox.information(
                self.ui, self.tr('Info'),
                self.tr(f'Cannot delete, reference by {userdata.name},{userdata.lastname}'))
            return
        self.main.session.delete(data)
        self.main.session.commit()
        tablemodel.refresh()

    def user_selected(self, index):
        """selected user

        :param index:
        :return:
        """
        pass

    def user_rang_refresh(self):
        users = self.main.session.query(model.User).order_by(model.User.bow_id).order_by(
            model.User.age_id).order_by(model.User.score.desc()).order_by(
            model.User.killpt.desc()).order_by(
            model.User.rate.desc()).all()
        save_bow_age = ['', '']
        rank = 1
        names_same_points = []
        same_points = [-1, -1, -1]
        for userdata in users:
            if (save_bow_age != [userdata.bowname, userdata.agename]):
                save_bow_age = [userdata.bowname, userdata.agename]
                rank = 1
                same_points = [-1, -1, -1]
            if same_points == [userdata.score, userdata.killpt, userdata.rate]:
                names_same_points.append(userdata.id)
                rank -= 1
            userdata.rank = rank
            rank += 1
            same_points = [userdata.score, userdata.killpt, userdata.rate]

        self.main.session.commit()
        users = self.main.session.query(model.User).order_by(model.User.bow_id).order_by(
            model.User.age_id).order_by(model.User.rank).all()
        return names_same_points, users

    def onprint(self, test=None):
        """Print Preview"""
        same_rank, users = self.user_rang_refresh()
        names = []
        names.append(self.tr('<h1>Overview</h1>'))
        save_bow_age = ['', '']
        for userdata in users:
            if save_bow_age != [userdata.bowname, userdata.agename]:
                names.append(f'<h2>{userdata.bowname}, {userdata.agename}</h2>')
                save_bow_age = [userdata.bowname, userdata.agename]
            names.append('{} {}, {}, {}, {}, {}, {}<br>'.format(
                userdata.rank,
                userdata.name,
                userdata.lastname,
                userdata.score,
                userdata.killpt,
                userdata.rate,
                userdata.clubname))
            if userdata.id in same_rank:
                names.append(self.tr('<p>Same rank</p>'))
        printdlg = DlgPrint(self.ui)
        printdlg.editor.setHtml("".join(names))
        if test:
            QTimer.singleShot(500, printdlg.reject)
        printdlg.exec()

    def on_overview(self, test=None):
        """Set the text for the info message box in html format
        To have a overview about the clubs with the members

        :returns: none
        """
        same_rank, users = self.user_rang_refresh()
        clubs = self.main.session.query(model.Club).order_by(model.Club.name).all()
        names = []
        names.append(self.tr('<h1>Overview</h1><h3>sorting by club</h3>'))
        for club in clubs:
            names.append(f'''
<p style="font-weight: bold";>{club.name}: {club.short}, {club.email},
Pay for: {club.payment} members {len(club.members)}:</p>''')
            if not club.payment == len(club.members):
                names.append(self.tr('<p style="color:red";>payment and club members are not even</p>'))
            for user in club.members:
                names.append(f'''
<p>{user.name} {user.lastname}: {user.agename}, {user.bowname} Rang:{user.rank} </p>''')
        names.append(self.tr('<h3>Rang:</h3>'))
        for user in users:
            names.append(f'''
<p>Rang:{user.rank} in {user.agename}, {user.bowname}: {user.name} {user.lastname} {user.clubname}</p>''')

        printdlg = DlgPrint(self.ui)
        printdlg.editor.setHtml("".join(names))
        if test:
            QTimer.singleShot(500, printdlg.reject)
        printdlg.exec()

    def createDockWindows(self):
        dock = QDockWidget(self.tr("Age"), self.ui)
        dock.setAllowedAreas(LeftDockWidgetArea | RightDockWidgetArea)
        ageWidget = QWidget(dock)
        layout = QVBoxLayout()

        self.ui.tableView_age = QTableView(dock)
        layout.addWidget(self.ui.tableView_age)

        self.ui.pushButton_age = QPushButton(self.tr('add new age'), dock)
        self.ui.pushButton_editage = QPushButton(self.tr('edit age'), dock)
        self.ui.pushButton_deleteage = QPushButton(self.tr('delete age'), dock)
        layout.addWidget(self.ui.pushButton_age)
        layout.addWidget(self.ui.pushButton_editage)
        layout.addWidget(self.ui.pushButton_deleteage)
        ageWidget.setLayout(layout)
        dock.setWidget(ageWidget)
        self.ui.addDockWidget(RightDockWidgetArea, dock)
        self.ui.viewMenu = self.ui.menuBar().addMenu(self.tr("&View"))
        self.ui.viewMenu.addAction(dock.toggleViewAction())

        dock = QDockWidget(self.tr("Bow"), self.ui)
        dock.setAllowedAreas(LeftDockWidgetArea | RightDockWidgetArea)
        ageWidget = QWidget(dock)
        layout = QVBoxLayout()

        self.ui.tableView_bow = QTableView(dock)
        layout.addWidget(self.ui.tableView_bow)

        self.ui.pushButton_bow = QPushButton(self.tr('add new bow'), dock)
        self.ui.pushButton_editbow = QPushButton(self.tr('edit bow'), dock)
        self.ui.pushButton_deletebow = QPushButton(self.tr('delete bow'), dock)
        layout.addWidget(self.ui.pushButton_bow)
        layout.addWidget(self.ui.pushButton_editbow)
        layout.addWidget(self.ui.pushButton_deletebow)
        ageWidget.setLayout(layout)
        dock.setWidget(ageWidget)
        self.ui.addDockWidget(LeftDockWidgetArea, dock)
        self.ui.viewMenu.addAction(dock.toggleViewAction())

        dock = QDockWidget(self.tr("Club"), self.ui)
        dock.setAllowedAreas(LeftDockWidgetArea | RightDockWidgetArea)
        ageWidget = QWidget(dock)
        layout = QVBoxLayout()

        self.ui.tableView_club = QTableView(dock)
        layout.addWidget(self.ui.tableView_club)

        self.ui.pushButton_club = QPushButton(self.tr('add new club'), dock)
        self.ui.pushButton_editclub = QPushButton(self.tr('edit club'), dock)
        self.ui.pushButton_deleteclub = QPushButton(self.tr('delete club'), dock)
        layout.addWidget(self.ui.pushButton_club)
        layout.addWidget(self.ui.pushButton_editclub)
        layout.addWidget(self.ui.pushButton_deleteclub)
        ageWidget.setLayout(layout)
        dock.setWidget(ageWidget)
        self.ui.addDockWidget(RightDockWidgetArea, dock)
        self.ui.viewMenu.addAction(dock.toggleViewAction())

        user_new = functools.partial(self.entry_new, model.User, self.main.model_user)
        club_new = functools.partial(self.entry_new, model.Club, self.main.model_club)
        age_new = functools.partial(self.entry_new, model.Age, self.main.model_age)
        bow_new = functools.partial(self.entry_new, model.Bow, self.main.model_bow)
        self.ui.pushButton_user.clicked.connect(user_new)
        self.ui.pushButton_club.clicked.connect(club_new)
        self.ui.pushButton_age.clicked.connect(age_new)
        self.ui.pushButton_bow.clicked.connect(bow_new)
        user_edit = functools.partial(self.entry_edit, model.User, self.main.model_user)
        club_edit = functools.partial(self.entry_edit, model.Club, self.main.model_club)
        age_edit = functools.partial(self.entry_edit, model.Age, self.main.model_age)
        bow_edit = functools.partial(self.entry_edit, model.Bow, self.main.model_bow)
        self.ui.pushButton_edituser.clicked.connect(user_edit)
        self.ui.pushButton_editclub.clicked.connect(club_edit)
        self.ui.pushButton_editage.clicked.connect(age_edit)
        self.ui.pushButton_editbow.clicked.connect(bow_edit)
        user_del = functools.partial(self.entry_delete, model.User, self.main.model_user)
        club_del = functools.partial(self.entry_delete, model.Club, self.main.model_club)
        age_del = functools.partial(self.entry_delete, model.Age, self.main.model_age)
        bow_del = functools.partial(self.entry_delete, model.Bow, self.main.model_bow)
        self.ui.pushButton_deleteuser.clicked.connect(user_del)
        self.ui.pushButton_deleteclub.clicked.connect(club_del)
        self.ui.pushButton_deleteage.clicked.connect(age_del)
        self.ui.pushButton_deletebow.clicked.connect(bow_del)

    def oninfo(self, test=None):
        """Set the text for the info message box in html format

        :returns: none
        """
        infobox = QtWidgets.QMessageBox(self.ui)
        infobox.setWindowTitle(self.tr('Info'))
        try:
            infobox.setWindowIcon(
                QtGui.QIcon(join(
                    "misc", "archerrank2.svg")))
        except FileNotFoundError:
            infobox.setWindowIcon(
                QtGui.QIcon(abspath(join(
                    dirname(sys.argv[0]), "misc", "archerrank2.svg"))))

        infobox.setText(self.tr(f'''
A tool for the evaluation of archery tournaments. Version {VERSION_STR}<br>
Archerrank2 is free software and use GNU General Public License
<a href="http://www.gnu.org/licenses/">www.gnu.org/licenses</a>'''))

        infobox.setInformativeText(self.tr('''
More Information about the program at <a href="https://github.com/MarkusHackspacher/Archerrank2">
github.com/MarkusHackspacher/Archerrank2</a>'''))

        if test:
            QTimer(infobox).singleShot(500, infobox.reject)
        infobox.exec()

    def on_create_winner(self):
        """create a word file with all to print"""
        savedfilename = self.main.session.query(model.Setting).filter_by(name='last_winner_file').first()
        if not savedfilename:
            lastdir = ''
        else:
            lastdir = savedfilename.value
        fileName, _ = QFileDialog.getSaveFileName(
                None, "QFileDialog.getSaveFileName()", lastdir,
                "Word Files (*.docx)")
        if fileName == '':
            return
        with MailMerge('input_winner.docx') as document:
            logging.info(document.get_merge_fields())
            users = self.main.session.query(model.User).order_by(model.User.club_id).all()
            winner = []
            for userdata in users:
                winner.append({'lastname': userdata.lastname,
                               'name': userdata.name,
                               'clubname': userdata.clubname,
                               'agename': userdata.agename,
                               'bowname': userdata.bowname})
            document.merge_pages(winner)
            document.write(fileName)
            logging.info(f'Save as {fileName}')
            if not savedfilename:
                self.main.session.add(model.Setting(name='last_winner_file', value=fileName))
            else:
                savedfilename.value = fileName
            self.main.session.commit()

    def on_create_adress(self, test=None):
        if (self.exportDir or not test):
            self.exportDir = QFileDialog.getExistingDirectory(
                None, self.tr("Open Directory"), "")
        with MailMerge('input_adress.docx') as document:
            logging.info(document.get_merge_fields())
            clubs = self.main.session.query(model.Club).order_by(model.Club.name).all()
            adress = []
            for userdata in clubs:
                logging.info(userdata.members)

                adress.append({'short': userdata.short,
                               'name': userdata.name,
                               'email': userdata.email,
                               'payment': str(userdata.payment),
                               'advertising': str(userdata.advertising),
                               'address': str(userdata.address),
                               'members': str(userdata.membersCount)})
            document.merge_pages(adress)
            document.write(self.exportDir + '\\output_adress.docx')
            logging.info('Save as output_adress.docx')
            infobox = QtWidgets.QMessageBox(self.ui)
            infobox.setWindowTitle(self.tr('Info'))
            infobox.setText(self.tr(f'''
export successful<br>
{self.exportDir}  output_adress.docx'''))
            if test:
                QTimer(infobox).singleShot(500, infobox.reject)
            infobox.exec()

    def on_xlsx_export(self, test=None):
        """export data in a xlsx file"""
        if (self.exportDir or not test):
            self.exportDir = QFileDialog.getExistingDirectory(
                None, self.tr("Open Directory"), "")

        xlsxexport = writexlsx.writexlsx()
        iterList = ('score', 'name', 'lastname', 'bowname', 'agename',
                    'clubname', 'killpt', 'rank', 'rate', 'other')
        xlsxexport.winner((iterList))
        users = self.main.session.query(model.User).order_by(model.User.score).all()
        for userdata in users:
            logging.info(userdata)
            xlsxexport.winner(
                tuple([getattr(userdata, x) for x in iterList]))

        iterList = ('clubname', 'name', 'lastname', 'bowname', 'agename',
                    'score', 'killpt', 'rank', 'rate', 'other')
        xlsxexport.user((iterList))
        users = self.main.session.query(model.User).order_by(model.User.club_id).all()
        for userdata in users:
            logging.info(userdata)
            xlsxexport.user(
                tuple([getattr(userdata, x) for x in iterList]))

        iterList = ('name', 'short', 'email', 'address', 'payment', 'advertising', 'membersCount')
        xlsxexport.adresse((iterList))
        clubs = self.main.session.query(model.Club).all()
        for userdata in clubs:
            logging.info(userdata)
            xlsxexport.adresse(
                tuple([getattr(userdata, x) for x in iterList]))

        iterList = ('name', 'short', 'sorting')
        xlsxexport.bow((iterList))
        bows = self.main.session.query(model.Bow).order_by(model.Bow.sorting).all()
        for userdata in bows:
            logging.info(userdata)
            xlsxexport.bow(
                tuple([getattr(userdata, x) for x in iterList]))

        iterList = ('name', 'short', 'adult', 'sep', 'sorting')
        xlsxexport.age((iterList))
        ages = self.main.session.query(model.Age).order_by(model.Age.sorting).all()
        for userdata in ages:
            logging.info(userdata)
            xlsxexport.age(
                tuple([getattr(userdata, x) for x in iterList]))

        try:
            xlsxexport.save('table.xlsx')
        except PermissionError:
            logging.info('Permission denied table.xlsx')
            infobox = QtWidgets.QMessageBox(self.ui)
            infobox.setWindowTitle(self.tr('Error'))
            infobox.setText(self.tr(f'''
Permission denied:<br>
{self.exportDir} table.xlsx'''))
            if test:
                QTimer(infobox).singleShot(500, infobox.reject)
            infobox.exec()
            return

        logging.info('Save as table.xlsx')
        infobox = QtWidgets.QMessageBox(self.ui)
        infobox.setWindowTitle(self.tr('Info'))
        infobox.setText(self.tr(f'''
export successful<br>
{self.exportDir} table.xlsx'''))
        if test:
            QTimer(infobox).singleShot(500, infobox.reject)
        infobox.exec()

    def on_exit(self):
        """exit and close

        :return:
        """
        self.ui.close()
