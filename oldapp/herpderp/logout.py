# -*- coding: utf-8 -*-
import app.lib.command

class Logout(app.lib.command.Command):
    name = "logout"

    def execute(self):
        self.session["user"] = None
        self.respond("Goodbye, %s." % (self.sender_nick,))
