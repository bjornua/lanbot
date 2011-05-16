# -*- coding: utf-8 -*-
import re
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
