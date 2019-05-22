#!/usr/bin/env python
# -*- coding: UTF-8 -*-
from flask import Flask, render_template, request, redirect, url_for, session
import re
import sqlite3
import hashlib
import base64
from classes import Database

import LocalConfig
filename = LocalConfig.filename

def md5(str):
    m = hashlib.md5()   
    m.update(str)
    return m.hexdigest()

def IfValidUrl(url):
    if re.match(r'^https?:/{2}\w.+$', url):
        if url.startswith('https://besthotvalentines.com') || url.startswith('http://besthotvalentines.com')
            return False
        else:
            return True
    else:
        return False

app = Flask(__name__)

def GenerateShort(LongAddr, digit):
    str = md5(LongAddr)
    str = base64.b64encode(str)
    return str[:digit]

@app.route('/', methods=['GET', 'POST'])
def home():
    LongAddr = ""
    ShortAddr = ""
    status = 0
    # status=0: Nothing input.
    # status=1: Input is not a valid url.
    # status=2: You are trying to visit a short address not existing in the database.
    if (request.method == 'POST'):
        LongAddr = request.form['LongAddr']
        if (not IfValidUrl(LongAddr)):
            status = 1
            return render_template('home.html', ShortAddr=ShortAddr, LongAddr=LongAddr, status=status)
        database = Database(filename)
        digit = 4;
        ShortAddr = GenerateShort(LongAddr,digit)
        search = database.find(ShortAddr)
        while(search != ''):
            if (search == LongAddr):
                break;
            else:
                digit = digit + 1
                ShortAddr = GenerateShort(LongAddr, digit)
                search = database.find(ShortAddr)
        if (search == ''):
            database.insert(ShortAddr, LongAddr)
        ShortAddr = 'http://hoogle.xyz/'+ShortAddr
    return render_template('home.html', ShortAddr=ShortAddr, LongAddr=LongAddr, status=status)

@app.route('/<ShortAddr>')
def visit(ShortAddr):
    database = Database(filename)
    LongAddr = database.find(ShortAddr)
    if (LongAddr == ''):
        return render_template('home.html', ShortAddr="", LongAddr="", status=2)
    else:
        return redirect(LongAddr)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
#    app.run()
