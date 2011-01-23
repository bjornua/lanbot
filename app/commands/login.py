# -*- coding: utf-8 -*-
import app.lib.command
import app.model.user

class Login(app.lib.command.Command):
    name = "login"
    require_auth = False
    
    def execute(self, username, password):
        "<username> <password>"
        
        if self.session.get("user") != None:
            self.respond("Error: Already logged in, please log out first")
            return
        
        id_ = app.model.user.authenticate(username, password)
        if id_ == None:
            self.respond("Could not recognize user %s with the given password. Not authed" % (username,))
            return
        
        self.session["user"] = id_
        
        self.respond("Authed as %s@%s" % (self.sender_nick, self.sender_host))

