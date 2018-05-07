#!/usr/bin/env python

from pandocfilters import toJSONFilter, RawBlock, Div, stringify
import re

def html(x):
    return RawBlock('html', x)

def latex(s):
    return RawBlock('latex', s)

def mk_columns(k, v, f, m):
    if k == "Para":
        value = stringify(v)
        if value.startswith('.') and value.endswith('['):
            return html(r'<div class="%s">' % value[1:-1])
        elif value == ".]":
            return html(r'</div>')

if __name__ == "__main__":
    toJSONFilter(mk_columns)
