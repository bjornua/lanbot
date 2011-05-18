# -*- coding: utf-8 -*-
import re

from app.modules.irc import client
from app.modules.utils.event import Events
from threading import Thread


quoted_string = r'"(([^"\\]|\\.)*)"'
normal_string = r'[^ ]+'

escchr = re.compile(r'(\\.)')
def escchrconvert(x):
    x = x.group(0)
    if x[1] in r'\"':
        return x[1]
    return x

p = re.compile("(%s)|(%s)" % (quoted_string, normal_string))
def parsecommand(s):
    args = []
    for x in p.findall(s):
        if x[3] != "":
            args.append(x[3])
        else:
            args.append(escchr.sub(escchrconvert, x[1]))

    return args

commands = {}
def registercommand(command):
    print "Added command: " + command.name
    commands[command.name] = command

def onmsg(msg):
    if not msg.text.startswith("!"):
        return

    tokens = parsecommand(msg.text[1:])
    if len(tokens) == 0:
        return
    
    command = tokens[0]
    args = tokens[1:]

    try:
        Command = commands[command]
    except KeyError:
        raise
    func = Command(msg)
    #func(*args)
    Thread(target=func, args=args).start()

client.event.add("chatmsg", onmsg)
