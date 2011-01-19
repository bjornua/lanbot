# -*- coding: utf-8 -*-
import re
quoted_string = r'"(([^"\\]|\\.)*)"'
normal_string = r'[^ ]+'
p = re.compile("(%s)|(%s)" % (quoted_string, normal_string))
def parse_command(s):
    return [x[1] or x[3] for x in p.findall(s)]

