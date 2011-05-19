# -*- coding: utf-8 -*-
import couchdb

def db():
    return couchdb.Server("http://127.0.0.1:5984")["lanbot"]
