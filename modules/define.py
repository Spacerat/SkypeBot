
import interface
import urllib2
from stringsafety import *
from xml.dom import minidom

def SetToken(str):
    global tokenstr
    token = str
    tokenstr = "tokenid="+token

tokenstr=''

def Handle(interface,command,args,messagetype):
    # @type args str
    url = "http://www.abbreviations.com/services/v1/"
    if command=='define':
        url+='syno.aspx?'+tokenstr+'&word='+URLSafe(args)
    else:
        url+='abbr.aspx?'+tokenstr+'&term='+URLSafe(args)
    request = urllib2.Request(url,None,{'Referer':'http://spacerat.meteornet.net'})
    response = urllib2.urlopen(request)
    data = minidom.parse(response)

    # @type data Document
    for top in data.childNodes:
        if top.childNodes:
            for result in top.childNodes:
                defin = result.getElementsByTagName("definition")[0].firstChild.data.capitalize()+"."
                term = string.capwords(result.getElementsByTagName("term")[0].firstChild.data)

                if command=='define':
                    part = result.getElementsByTagName("partofspeach")[0].firstChild.data
                    interface.Reply("http://www.definitions.net/definition/"+URLSafe(args))
                    interface.Reply("{0} ({1})".format(term,part))
                    interface.Reply(defin)
                    break
                elif command=='abbr':
                    cat = result.getElementsByTagName("category")[0].firstChild.data
                    if cat == 'Adult' or cat == 'Chat' or cat == 'SMS' or cat == 'File Extensions':
                        interface.Reply("http://www.abbreviations.com/"+URLSafe(args))
                        interface.Reply("{0} ({1})".format(term,cat))
                        interface.Reply(defin)
                        break

interface.AddHook("define",Handle,"DefineBot")
interface.AddHook("abbr",Handle,"DefineBot")

