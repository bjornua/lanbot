# -*- coding: utf-8 -*-
import re

from app.modules.irc import client
from app.modules.utils.event import Events

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

def register_command(command):
    commands[command.name]:

def onmsg(msg):
    print(parsecommand(msg.text))

client.event.add("chatmsg", onmsg)
