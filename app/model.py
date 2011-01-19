# -*- coding: utf-8 -*-
from app.utils import db



def getuserid(username, password):
    result = db().view("user/auth", include_doc=True, limit=1)
    for row in result:
        return row.id

