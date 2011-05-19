# -*- coding: utf-8 -*-
import httplib
import urllib
from app.modules.command.base import BaseCommand
from app.modules.command import registercommand

from threading import Thread

def query(q, msg):
    path = "/search?" + urllib.urlencode({"q": q}) + "&hl=da&btnI&safe=off"
    conn = httplib.HTTPConnection("www.google.com")
    headers = {"Referer": "http://www.google.com/", "Connection": "close"}
    conn.request("GET", path, "", headers)
    response = conn.getresponse()
    conn.close()
    return response.getheader("Location")

class Google(BaseCommand):
    name = "google"
    
    def exists(self):
        return True
    def __call__(self, *args):
        if len(args) == 0:
            return
        result = query('"' + '" "'.join(args) + '"' , self.msg)
        self.msg.reply(result)

registercommand(Google)
