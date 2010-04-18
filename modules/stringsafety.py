
import re

# Courtasy of Katharine :3

def escapeurl(url,plus=False):
    safe = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_-'
    output = ''
    for char in url:
        if char in safe:
            output += char
        elif char==' ' and plus==True:
            output += '+'
        else:
            code = hex(ord(char))[2:]
            while len(code) > 0:
                if len(code) == 1:
                    code = '0' + code
                output += '%' + code[0:2]
                code = code[2:]
    return output

def FormatHTML(data):
    p = re.compile(r'<.*?>')
    data = p.sub('', data)
    data = data.replace("&quot;",'"')
    data = data.replace("&#39;","'")
    return data