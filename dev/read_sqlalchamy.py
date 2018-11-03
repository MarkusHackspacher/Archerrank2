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
from sqlalchemy import orm, literal,  create_engine

import sys
sys.path.append('..')

from modules import model


# Create an engine and create all the tables we need
engine = create_engine('sqlite:///../test2.sqlite', echo=False)
model.base.metadata.bind = engine
model.base.metadata.create_all(engine)

# Set up the session
sm = orm.sessionmaker(bind=engine,
                      autoflush=True,
                      autocommit=True,
                      expire_on_commit=True)
session = orm.scoped_session(sm)


if not session.query(model.Club).all():
    session.add(model.Club(name='VfB Stuttgart', short='VfB'))
if not session.query(model.Age).all():
    session.add(model.Age(name='Best of All', short='Elite'))
if not session.query(model.Bow).all():
    session.add(model.Bow(name='Longbow', short='LB'))
if not session.query(model.User).all():
    session.add(model.User(name='John', lastname='Dow', club_id=1, age_id=1, bow_id=1))


print(session.query(model.Age).first())
print(session.query(model.Bow).first())
print(session.query(model.User).first())

#session.add(model.Club(name='fakename', short='fake'))
#session.add(model.Age(name='fakename', short='fake'))

print(session.query(model.Club).first())
session.query(model.Club).first().short='asdydfedf'
#session.commit()
print(session.query(model.Age).all())
print(session.query(model.Club).all())