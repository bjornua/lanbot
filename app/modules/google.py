# -*- coding: utf-8 -*-
import httplib
import urllib
import app.modules.command.base
import app.modules.command

def query(q, msg):
    path = "/search?" + urllib.urlencode({"q": q}) + "&hl=da&btnI&safe=off"
    conn = httplib.HTTPConnection("www.google.com")
    headers = {"Referer": "http://www.google.com/", "Connection": "close"}
    print "1"
    msg.reply("Looking up: " + q)
    conn.request("GET", path, "", headers)
    print "2"
    response = conn.getresponse()
    conn.close()
    return response.getheader("Location")

class GoogleCommand(app.modules.command.base.BaseCommand):
    name = "google"
    
    def exists(self):
        return True
    def __call__(self, *args):
        if len(args) == 0:
            return
        result = query('"' + '" "'.join(args) + '"' , self.msg)
        self.msg.reply(result)


app.modules.command.registercommand(GoogleCommand)

