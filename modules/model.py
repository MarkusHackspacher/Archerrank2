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

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

# https://docs.sqlalchemy.org/en/latest/orm/tutorial.html
from sqlalchemy.ext.declarative import declarative_base

base = declarative_base()


class User(base):
    """characteristics of the user table"""
    __tablename__ = 'users'
    nr = Column(Integer, primary_key=True)
    lastname = Column(String)
    name = Column(String)
    club = Column(String)
    score = Column(Integer)
    kills = Column(Integer)

    age = relationship("CupWinnerBet",
                                   order_by="CupWinnerBet.id",
                                   backref="users")
    bow = relationship("GameBet", order_by="GameBet.id",
                             backref="users")
    part = Column(Integer)
    rate = Column(Integer)
    other = Column(String)

    def __repr__(self):
        return "<User(name='{0}', fullname='{1}', club='{2}')>".format(
            self.name, self.lastname, self.club)


class Age(base):
    """characteristics of the team table"""
    __tablename__ = 'ages'
    age = Column(Integer, primary_key=True)
    short = Column(String)
    name = Column(String)
    sep = Column(Integer)
    adult = Column(Integer)
    pos = Column(Integer)

    def __repr__(self):
        return ("<Age(name='{0}', short='{1}', adult='{2}' sep='{3}'".
                format(self.name, self.short, self.adult, self.sep))


class Bow(base):
    """characteristics of the competition table"""
    __tablename__ = 'bows'
    bow = Column(Integer, primary_key=True)
    short = Column(String)
    name = Column(String)
    pos = Column(Integer)

    def __repr__(self):
        return ("<Bow(name='{0}', short='{1}' pos='{2}'".
                format(self.name, self.short, self.pos))


class Setting(base):
    """characteristics of the cup winner bet table"""
    __tablename__ = 'settings'
    name = Column(String)
    value = Column(String)

    def __repr__(self):
        return ("<Setting(name='{0}', value='{1}')>".
                format(self.name, self.value))
