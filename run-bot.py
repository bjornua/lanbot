#!/usr/bin/python2 -B
# -*- coding: utf-8 -*-
import app.bot

bot = app.bot.LANBot("irc.freenode.net", 6667)

bot.client.nick("LANBot")
bot.client.user("LANBot", "ignored", "ignored", "ignored")

bot.client.loop()
