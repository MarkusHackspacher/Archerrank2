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

import unittest

from sqlalchemy import create_engine, orm

from modules import model


class TestCodeFormat(unittest.TestCase):
    """
    Test of the code format
    """
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

    def test_user_model(self):
        """Test the user model
        """
        ed_user = model.User(name='Ed', lastname='Jones')
        self.session.add(ed_user)
        our_user = self.session.query(model.User).filter_by(name='Ed').first()
        self.assertEqual(our_user.name, 'Ed')
        self.assertEqual(our_user.lastname, 'Jones')
        print(self.session.query(model.User).first())
        self.assertEqual(our_user.clubname, None)
        self.assertEqual(our_user.agename, None)
        self.assertEqual(our_user.bowname, None)

    def test_age_model(self):
        """Test the age model
        """
        self.session.add(model.Age(name='young talented', short='advanced'))
        our_age = self.session.query(model.Age).filter_by(
                name='young talented').first()
        self.assertEqual(our_age.name, 'young talented')
        self.assertEqual(our_age.short, 'advanced')
        self.assertEqual(our_age.sep, 1)
        self.assertEqual(our_age.adult, 1)
        self.assertEqual(our_age.sorting, 0)
        print(self.session.query(model.Age).first())

    def test_bow_model(self):
        """Test the bow model
        """
        self.session.add(model.Bow(name='long bow', short='long'))
        our_bow = self.session.query(model.Bow).filter_by(
                name='long bow').first()
        self.assertEqual(our_bow.name, 'long bow')
        self.assertEqual(our_bow.short, 'long')
        self.assertEqual(our_bow.sorting, 0)
        print(self.session.query(model.Bow).first())

    def test_club_model(self):
        """Test the club model
        """
        self.session.add(model.Club(name='long bow club', short='long'))
        our_club = self.session.query(model.Club).filter_by(
                name='long bow club').first()
        self.assertEqual(our_club.name, 'long bow club')
        self.assertEqual(our_club.short, 'long')
        self.assertEqual(our_club.email, None)
        self.assertEqual(our_club.address, None)
        self.assertEqual(our_club.payment, 0)
        self.assertEqual(our_club.advertising, 0)
        print(self.session.query(model.Club).first())

    def test_setting_model(self):
        """Test the setting model
        """
        self.session.add(model.Setting(name='lastlayout', value='long'))
        our_set = self.session.query(model.Setting).filter_by(
                name='lastlayout').first()
        self.assertEqual(our_set.name, 'lastlayout')
        self.assertEqual(our_set.value, 'long')
        print(self.session.query(model.Setting).first())
