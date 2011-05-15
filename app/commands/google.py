import app.lib.command
import httplib
import urllib

def query(q):
    path = "/search?" + urllib.urlencode({"q": q}) + "&hl=da&btnI&safe=off"
    conn = httplib.HTTPConnection("www.google.com")
    headers = {"Referer": "http://www.google.com/"}
    conn.request("GET", path, None, headers)
    response = conn.getresponse()
    conn.close()
    return response.getheader("Location")

class Command(app.lib.command.BaseCommand):
    name = "google"
    
    def exists(self):
        return True
    
    def __call__(self, *args):
        if len(args) == 0:
            return
        self.msg.reply(query('"' + '" "'.join(args) + '"'))
