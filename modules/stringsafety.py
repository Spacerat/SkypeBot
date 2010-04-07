
import string
import re



def URLSafe(str):

    urlsafepattern = re.compile(r'[^'+string.letters+string.digits+r'_-]\%', re.VERBOSE)
    str = str.replace("%","%25")
    str = str.replace(" ","%20")
    str = str.replace("!","%21")
    str = str.replace('"',"%22")
    str = str.replace("#","%23")
    str = str.replace("$","%24")
    str = str.replace("&","%26")
    str = str.replace("'","%27")
    str = str.replace("(","%28")
    str = str.replace(")","%29")
    str = str.replace("*","%2A")
    str = str.replace("+","%2B")
    str = str.replace(",","%2C")
    str = str.replace("-","%2D")
    str = str.replace(".","%2E")
    str = str.replace("/","%2F")
    str = re.sub(urlsafepattern, "", str)
    return str

def FormatHTML(data):
    p = re.compile(r'<.*?>')
    data = p.sub('', data)
    data = data.replace("&quot;",'"')
    data = data.replace("&#39;","'")
    return data