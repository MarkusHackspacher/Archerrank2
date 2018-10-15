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

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.types import TEXT
# https://docs.sqlalchemy.org/en/latest/orm/tutorial.html
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()


class User(base):
    """characteristics of the user table"""
    __tablename__ = 'users'
    nr = Column(Integer, primary_key=True)
    lastname = Column(TEXT)
    name = Column(TEXT)
    club_id = Column(Integer, ForeignKey('clubs.short'))
    score = Column(Integer, default=0)
    kills = Column(Integer, default=0)

    age_id = Column(Integer, ForeignKey('ages.age'))
    bow_id = Column(Integer, ForeignKey('bows.bow'))
    part = Column(Integer, default=1)
    rate = Column(Integer, default=1)
    other = Column(TEXT)

    def __repr__(self):
        return ("<User(name='{0}', fullname='{1}', club='{2}', age='{3}', bow='{4}')>"
            .format(self.name, self.lastname, self.club_id.short, self.age_id.name, self.bow_id.name))


class Age(base):
    """characteristics of the age grade table"""
    __tablename__ = 'ages'
    age = Column(Integer, primary_key=True)
    short = Column(TEXT)
    name = Column(TEXT)
    sep = Column(Integer, default=1)
    adult = Column(Integer, default=1)
    pos = Column(Integer, default=0)

    def __repr__(self):
        return ("<Age(name='{0}', short='{1}', adult='{2}' sep='{3}'".
                format(self.name, self.short, self.adult, self.sep))


class Bow(base):
    """characteristics of the bow grade table"""
    __tablename__ = 'bows'
    bow = Column(Integer, primary_key=True)
    short = Column(TEXT)
    name = Column(TEXT)
    pos = Column(Integer, default=0)

    def __repr__(self):
        return ("<Bow(name='{0}', short='{1}' pos='{2}'".
                format(self.name, self.short, self.pos))


class Setting(base):
    """characteristics of the setting table"""
    __tablename__ = 'settings'
    name = Column(TEXT, primary_key=True)
    value = Column(TEXT)

    def __repr__(self):
        return ("<Setting(name='{0}', value='{1}')>".
                format(self.name, self.value))

class Club(base):
    """characteristics of the club table
    payment: have pay for x players
    advertising: 0 not set
                 1 no advertising, no save address for further use
                 2 can save address
                 3 by email
                 4 by letter
                 5 by email and letter
    """
    __tablename__ = 'clubs'
    short = Column(TEXT, primary_key=True)
    name = Column(TEXT)
    email = Column(TEXT)
    address = Column(TEXT)
    payment = Column(Integer, default=0)
    advertising = Column(Integer, default=0)

    def __repr__(self):
        return ("<Club(short='{0}', name='{1}', payment'{2}')>".
                format(self.short, self.name, self.payment))
