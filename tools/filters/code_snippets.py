#!/usr/bin/env python

from pandocfilters import toJSONFilter, RawBlock, Div, stringify
import re

def html(x):
    return RawBlock('html', x)

def latex(s):
    return RawBlock('latex', s)

def convert_cb(k, v, f, m):
    if k == 'CodeBlock':
        [[ident, classes, keyvals], code] = v
        #print("++",ident,classes,keyvals)
        rvalue = r'<pre><code'
        if len(classes) > 0:
            rvalue += r' class="%s"' % classes[0]
        if len(keyvals) > 0:
            for item in keyvals:
                if len(item) > 1:
                    rvalue += r' '
                    rvalue += item[0]
                    rvalue += r'='
                    if "style" in item[0]:
                        rvalue += r'"'
                    rvalue += item[1]
                    if 'style' in item[0]:
                        rvalue += r'"'

                if len(item) == 1:
                    rvalue += r' %s' % (item[0])
        # data-trim data-noescape>\n'#TODO: would love to get rid of this, but fenced_code_attributes considers this a Para if they appear in the CodeBlock header
        rvalue += '>\n'
        rvalue += code
        rvalue += '\n'
        rvalue += "</code></pre>"
        return html(rvalue)

if __name__ == "__main__":
    toJSONFilter(convert_cb)
