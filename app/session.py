# -*- coding: utf-8 -*-

class Session(object):
    def __init__(self, id):
        self.id = id
        self.is_init = False
        self.changed = False
    
    def init(self):
        if self.is_init:
            return
        self.is_init = True
        
        if not self.load_session():
            self.new_session()
    
    def load_session(self):
        try:
            self.doc = list(db().view("session/by_id", key=self.id, include_docs=True))[0].doc
            return True
        except IndexError:
            return False
        
    def new_session(self):
        self.doc = {"id": self.id, "type": "session", "data":{}}
    
    def save(self):
        if not self.changed:
            return
        self.id, self.doc["_rev"] = db().save(self.doc)
    
    def get(self, *args, **kwargs):
        self.init()
        return self.doc["data"].get(*args,**kwargs)
    
    def __setitem__(self, *args, **kwargs):
        self.init()
        self.changed = True
        return self.doc["data"].__setitem__(*args,**kwargs)

