# -*- coding: utf-8 -*-
from app.config.generated import config
import couchdb

def db():
    return couchdb.Server(config["couchdb_server_url"])[config["couchdb_db"]]

