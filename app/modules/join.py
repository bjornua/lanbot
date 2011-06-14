from app.modules.irc import writer, parser
from app.modules.command import registercommand
from app.modules.command.base import BaseCommand


class Join(BaseCommand):
    name = "join"

    def texttochannel(self, name):
        if not (name.startswith("#") or name.startswith("&")):
            return

        for x in (chr(7), " ", ","):
            if x in name:
                return

        return name

    def __call__(self, textchannel):
        channel = self.texttochannel(textchannel)
        if channel == None:
            self.msg.reply("Kanalens navn er ugyldigt: " + textchannel)
            return
        
        self.msg.reply(repr(channel))
        writer.join(channel)

#Lets not do that without authentication
#registercommand(Join)
