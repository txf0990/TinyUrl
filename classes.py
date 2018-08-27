#!/usr/bin/end python
# -*- encoding: utf-8 -*-
import sqlite3

import string
import random
import re
class Database(object):
    'This is the database'
    def __init__(self, filename):
        self.conn = sqlite3.connect(filename)
        self.c = self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS AddressMap (ShortAddr text PRIMARY KEY, LongAddr text)")
        self.conn.commit()

    def insert(self, ShortAddr, LongAddr):
        self.c.execute('INSERT INTO AddressMap(ShortAddr,LongAddr) Values(?,?)',(ShortAddr, LongAddr))
        self.conn.commit()

    def find(self, ShortAddr):
        cursor_object = self.c.execute('SELECT * FROM AddressMap WHERE ShortAddr=?', (ShortAddr,))
        list_cursor_object = list(cursor_object)        # list_cursor_object is a list of tuple.
        if len(list_cursor_object) == 0:
            return ""
        else:
            return list_cursor_object[0][1]

