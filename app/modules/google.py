# -*- coding: utf-8 -*-
import httplib
import urllib
import app.modules.command.base
import app.modules.command

def query(q):
    print "ji"
    path = "/search?" + urllib.urlencode({"q": q}) + "&hl=da&btnI&safe=off"
    print "ji1"
    conn = httplib.HTTPConnection("www.google.com")
    print "ji2"
    headers = {"Referer": "http://www.google.com/", "Connection": "close"}
    print "ji3"
    conn.request("GET", path, None, headers)
    print "ji4"
    response = conn.getresponse()
    print "ji5"
    conn.close()
    print "ji6"
    return response.getheader("Location")

class GoogleCommand(app.modules.command.base.BaseCommand):
    name = "google"
    
    def exists(self):
        return True
    
    def __call__(self, *args):
        if len(args) == 0:
            return
        print "3"
        result = query('"' + '" "'.join(args) + '"')
        print "4"
        self.msg.reply(result)
        print "5"


app.modules.command.registercommand(GoogleCommand)

