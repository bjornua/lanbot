# -*- coding: utf-8 -*-
import now
import google
import fart
import join
commands = {}

for module in (
    now,
    google,
    fart,
    join,
):
    command = module.Command
    print "Adding command: " + command.name
    commands[command.name] = command
