#!/usr/bin/python2 -B
# -*- coding: utf-8 -*-
import app.bot

while True:
    bot = app.bot.LANBot("LANBot")
    print "Connecting to irc.freenode.net:6667"
    bot.client.start("irc.freenode.net", 6667)
    print "Disconnected"
