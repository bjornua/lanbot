# -*- coding: utf-8 -*-
from app.utils import db

class Session(object):
    def __init__(self, nick, host):
        self.nick = nick
        self.host = host
        self.is_init = False
        self.changed = False
    
    def init(self):
        if self.is_init:
            return
        self.is_init = True
        
        if not self.load_session():
            self.new_session()
    
    def load_session(self):
        for row in db().view("session/by_sender", include_docs=True)[self.nick, self.host]:
            self.doc = row.doc
            return True
        return False
        
    def new_session(self):
        self.doc = {
            "nickname": self.nick,
            "host": self.host,
            "type": "session",
            "data": {}
        }
    
    def save(self):
        if not self.is_init:
            return
        self.doc["_id"], self.doc["_rev"] = db().save(self.doc)
    
    def get(self, *args, **kwargs):
        self.init()
        return self.doc["data"].get(*args,**kwargs)
    
    def __setitem__(self, *args, **kwargs):
        self.init()
        return self.doc["data"].__setitem__(*args,**kwargs)
