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
from sqlite3 import Error
from flask import g
# import secrets ### requires python 3.6^
import random
import json
from flask import jsonify


#dbfile = '/var/www/flask/p/track_metadata.db'
dbfile = '/Users/dw/Dropbox/GitHub/pi/www/flask/p/track_metadata.db'

#/Users/dw/pi/www/flask/p/lastfm_similars.db


print("metadata file go")


def die_with_usage():
    """ HELP MENU """
    print('demo_similars_db.py')
    print('  by T. Bertin-Mahieux (2011) tb2332@columbia.edu')
    print('')
    print('Shows how to use the SQLite database made from similar')
    print('tracks in the Last.fm dataset.')
    print('')
    print('USAGE:')
    print('  ./demo_similars_db.py <similars.db>')


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

def get_artists_flask_tut():
    print("running get_artists_flask_tut")
    artistlist = []
    # artist_json = {}
    count = 0
    for artist_name in query_db('select distinct artist_name from songs order by artist_name;'):
        # print(artist_name[0])
        # artistlist = artistlist+"artist="+artist_name[0]+",\n"
        # artistlist.append("artist=")
        # artistlist.append(artist_name[0])
        item = {"artist": artist_name[0]}
        artistlist.append(item)
        # print(artistlist)
        # artistlist.append(",")
        # artistlist.append(

        # artist_json['name'] = artist_name[0]
    print(artistlist)
    return artistlist
    json_data = json.dumps(artistlist)
    return json_data
    # print(artistlist)
    # return artistlist

def get_all_songs_by_artist(artist):
    print("query to db is: '%s'" % artist)
    tracklist = []
    for tracknames in query_db("select distinct title from songs where artist_name = '%s';" % artist):
        print(tracknames)
        print(type(tracknames))
        print(tracknames[0])
        tracklist.append(tracknames[0])
    return tracklist

def get_related_song_flask(tid):
    print("attempting flask related song query style")
    sql = "SELECT target FROM similars_src WHERE tid='%s'" % tid
    answer = query_db(sql)
    value = random(1, 5)
    song = answer[value]
    print("printing song /n", song)
    return(song)


### end flask tutorial styled functions

def get_artist_from_track_id(tid):
    conn = sqlite3.connect(dbfile)
    # tid = 'TREDTHC128F92D42F0'
    print("Attempting to get artist from track id")
    sql = "SELECT artist_name FROM songs WHERE track_id = '%s'" % tid
    res = conn.execute(sql)
    data = res.fetchone()[0]
    print("going to print data type")
    print(type(data))
    print(data)
    return data

def get_all_artists():
    conn = sqlite3.connect(dbfile)
    # tid = 'TREDTHC128F92D42F0'
    print("Attempting to get all artists")
    sql = "SELECT artist_name FROM songs ORDER BY artist_name"
    res = conn.execute(sql)
    data = res.fetchone() # [0]
    for i in enumerate(data):
        print(i)
    # print(data)
    return data


def get_related_track(tid):
    print("seriously, get_related_track has been called")
    conn = sqlite3.connect(dbfile)
    #tid = 'TREDTHC128F92D42F0'
    print('We get all similar songs (with value) to %s' % tid)
    sql = "SELECT target FROM similars_src WHERE tid='%s'" % tid
    res = conn.execute(sql)
    data = res.fetchone()[0]
    # print(data)
    # random_choice = secrets.choice(data)
    print(type(data))
    value = random.randint(0, 5)
    return data[value]
    # return data.partition(',')[0]


def dbTestFunction():

    # input test
    if not os.path.isfile(dbfile):
        print('ERROR: db file %s does not exist?' % dbfile)
        die_with_usage()

    # open connection
    conn = sqlite3.connect(dbfile)
    print("connection may be established")


    # EXAMPLE 1
    print('************** DEMO 1 **************')
    tid = 'TREDTHC128F92D42F0'
    print('We get all similar songs (with value) to %s' % tid)
    sql = "SELECT target FROM similars_src WHERE tid='%s'" % tid
    res = conn.execute(sql)
    data = res.fetchone()[0]
    print(data)
    print('total number of similar tracks:  %d' % (len(data.split(','))/2))

    # EXAMPLE 2
    print('************** DEMO 2 **************')
    tid = 'TRCXCLD128F93127D3'
    print('We get all songs which consider %s as similar' % tid)
    sql = "SELECT target FROM similars_dest WHERE tid='%s'" % tid
    res = conn.execute(sql)
    data = res.fetchone()[0]
    print(data)
    print('total number of track where %s is similar: %d' % (tid,
          len(data.split(','))/2))

    # EXAMPLE 3
    print('************** DEMO 3 **************')
    print('We count the number of songs with at least one known similar')
    sql = "SELECT DISTINCT tid FROM similars_src"
    res = conn.execute(sql)
    cnt = len(res.fetchall())
    print('Found %d such tracks' % cnt)

    # EXAMPLE 4
    print('************** DEMO 4 **************')
    print('We count the number of unique songs who are considered similar to some other one')
    sql = "SELECT DISTINCT tid FROM similars_dest"
    res = conn.execute(sql)
    cnt = len(res.fetchall())
    print('Found %d such tracks' % cnt)

    # EXAMPLE 5
    print('************** DEMO 5 **************')
    tid = 'TRPYHPC128F930F9B0'
    print('We get similars to %s and order them by similarity value' % tid)

    sql = "SELECT target FROM similars_dest WHERE tid='%s'" % tid
    res = conn.execute(sql)
    data = res.fetchone()[0]
    data_unpacked = []
    for idx, d in enumerate(data.split(',')):
        if idx % 2 == 0:
            pair = [d]
        else:
            pair.append(float(d))
            data_unpacked.append(pair)
    # sort
    data_unpacked = sorted(data_unpacked, key=lambda x: x[1], reverse=True)
    for k in range(10):
        print(data_unpacked[k])
    print('...')
    print('total number of pairs with such similarity value: %s' % len(data_unpacked))

    # close connection
    conn.close()

# dbTestFunction()
