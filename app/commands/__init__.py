# -*- coding: utf-8 -*-
import now
import google
import fart
commands = {}

for module in (
    now,
    google,
    fart,
):
    command = module.Command
    print "Adding command: " + command.name
    commands[command.name] = command
