#!/usr/bin/env python
"""
Thierry Bertin-Mahieux (2011) Columbia University
tb2332@columbia.edu


This code shows how to use the SQLite database made with similar
tracks from the Last.fm dataset.
Code developed using python 2.6 on an Ubuntu machine, utf-8 by default.

This is part of the Million Song Dataset project from
LabROSA (Columbia University) and The Echo Nest.


Copyright 2011, Thierry Bertin-Mahieux <tb2332@columbia.edu>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import os
import sys
import sqlite3
import random
from sqlite3 import Error
from flask import g
import secrets
from flask import jsonify
from marshmallow import Schema, fields

# dbfile = '/var/www/flask/p/lastfm_similars.db'
dbfile = '/Users/dw/pi/www/flask/p/lastfm_similars.db'

#/Users/dw/pi/www/flask/p/lastfm_similars.db


print("db file go")


class AlbumSchema(Schema):
    class Meta:
        fields = ("songid", "chance")


# if __name__ == '__main__':
def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return None

def getRelatedTrack(tid):
    conn = sqlite3.connect(dbfile)
    #tid = 'TREDTHC128F92D42F0'
    print('We get all similar songs (with value) to %s' % tid)
    sql = "SELECT target FROM similars_src WHERE tid='%s'" % tid
    res = conn.execute(sql)
    data = res.fetchone()[0]

    # get the top 5 matched id's in a list
    data2 = data.split(',')[0:9:2]
    # return a random id from the top 5 matches last
    value = random.randint(0,5)
    return data2[value]


#### flask tutorial styled functions

# @app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def get_db():
    db = getattr(g, 'dbfile', None)
    if db is None:
        db = g._database = sqlite3.connect(dbfile)
    return db

def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

def get_related_song_flask(tid):
    print("attempting flask related song query style")
    sql = "SELECT target FROM similars_src WHERE tid='%s'" % tid
    answer = query_db(sql)
    value = random.randint(0, 4)
    song = answer[4]
    print("song type is ", type(song))
    print("printing song ", song)

    return jsonify(song)


### end flask tutorial styled functions


