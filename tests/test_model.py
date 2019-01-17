# -*- coding: utf-8 -*-

# archerrang2

# Copyright (C) <2019> Markus Hackspacher

# This file is part of archerrang2.

# archerrang2 is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# archerrang2 is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with archerrang2.  If not, see <http://www.gnu.org/licenses/>.

import unittest
from sqlalchemy import orm
from sqlalchemy import create_engine
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

    def test_age_model(self):
        """Test the age model
        """
        session.add(model.Age(name='young talented', short='advanced'))
        our_team = self.session.query(model.Age).filter_by(
                name='young talented').first()
        self.assertEqual(our_team.name, 'young talented')
        self.assertEqual(our_team.short , 'advanced')
        self.assertEqual(our_team.sep, 1)
        self.assertEqual(our_team.adult, 1)
        self.assertEqual(our_team.sorting , 0)

    def test_bow_model(self):
        """Test the bow model
        """
        session.add(model.Bow(name='long bow', short='long'))
        our_team = self.session.query(model.Bow).filter_by(
                name='long bow').first()
        self.assertEqual(our_team.name, 'long bow')
        self.assertEqual(our_team.short , 'long')
        self.assertEqual(our_team.sorting , 0)

    def test_club_model(self):
        """Test the club model
        """
        session.add(model.Club(name='long bow club', short='long'))
        our_team = self.session.query(model.Club).filter_by(
                name='long bow club').first()
        self.assertEqual(our_team.name, 'long bow club')
        self.assertEqual(our_team.short , 'long')
        self.assertEqual(our_team.email  , '')
        self.assertEqual(our_team.address  , '')
        self.assertEqual(our_team.payment  , 0)
        self.assertEqual(our_team.advertising  , 0)
