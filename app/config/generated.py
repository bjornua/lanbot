# -*- coding: utf-8 -*-
from app.config.default import config
config = config()
config.update({'couchdb_server_url': 'http://127.0.0.1:5984/', 'couchdb_db': 'lanbot'})