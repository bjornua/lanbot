# -*- coding: utf-8 -*-
import now
import google
import fart
import join
import leave
import msg
commands = {}

for module in (
    now,
    google,
    fart,
    join,
    leave,
    msg,
):
    command = module.Command
    print "Adding command: " + command.name
    commands[command.name] = command
