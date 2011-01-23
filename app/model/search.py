# -*- coding: utf-8 -*-
from app.utils import db
from app.lib.date import fromtuple
import couchdb

def search(channel, word):
    result = db().view("chanmsg/search", 
        include_docs=True,
        limit=1,
        startkey=[channel, word],
        endkey=[channel, word + u"\u9999"],
    )
    
    for row in result:
        doc = row.doc
        time = fromtuple(doc["time"])
        sender = doc["sender_nick"]
        msg = doc["msg"] 
        
        return time, sender, msg 
