
import interface
import urllib2
from stringsafety import *
from xml.dom import minidom
import string

def SetToken(str):
    global tokenstr
    token = str
    tokenstr = "tokenid="+token

tokenstr=''

def Handle(interface,command,args,messagetype):
    """!define word - Gets the definition of a word
    !abbr abbreviation - Gets the expansion of an abbreviation"""
    # @type args str
    if args.strip()=="":
        interface.Reply("Use %sdefine word" % interface.GetPrefix())
        return
    url = "http://www.abbreviations.com/services/v1/"
    if command=='define':
        url+='syno.aspx?'+tokenstr+'&word='+escapeurl(args)
    else:
        url+='abbr.aspx?'+tokenstr+'&term='+escapeurl(args)
    request = urllib2.Request(url,None,{'Referer':'http://spacerat.meteornet.net'})
    response = urllib2.urlopen(request)
    data = minidom.parse(response)

    # @type data Document
    for top in data.childNodes:
        if top.childNodes and len(top.childNodes)>0:
            for result in top.childNodes:
                defin = result.getElementsByTagName("definition")[0].firstChild.data.capitalize()+"."
                term = string.capwords(result.getElementsByTagName("term")[0].firstChild.data)

                if command=='define':
                    part = result.getElementsByTagName("partofspeach")[0].firstChild.data
                    interface.Reply("http://www.definitions.net/definition/"+escapeurl(args))
                    interface.Reply("{0} ({1})".format(term,part))
                    interface.Reply(defin)
                    break
                elif command=='abbr':
                    cat = result.getElementsByTagName("category")[0].firstChild.data
                    if cat == 'Adult' or cat == 'Chat' or cat == 'SMS' or cat == 'File Extensions':
                        interface.Reply("http://www.abbreviations.com/"+escapeurl(args))
                        interface.Reply("{0} ({1})".format(term,cat))
                        interface.Reply(defin)
                        break
        else:
            interface.Reply('No definition found for '+args)


interface.ComHook("define",Handle,name="DefineBot")
interface.ComHook("abbr",Handle,name="DefineBot")
