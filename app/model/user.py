# -*- coding: utf-8 -*-
from app.utils import db
from app.lib.date import nowtuple
import couchdb

class UserExists(Exception):
    pass

def authenticate(username, password):
    result = db().view("user/auth", 
        include_doc=True,
        key=[username, password],
    )
    
    for row in result:
        return row.id

def getid(username):
    for row in db().view("user/auth", limit=1)[username:]:
        if(row.key[0] != username):
            return
        return row.id


def create(username, password):
    userid = getid(username)
    if not userid == None:
        raise UserExists("User %s exists with id %s" % (repr(username), repr(userid)))
    user = {
        "type": "user",
        "time_created": nowtuple(),
        "username": username,
        "password": password,
    }
    return db().save(user)[0]
    
def remove(username):
    userid = getid(username)
    
    if userid == None:
        return False
    del db()[userid]
    return True


