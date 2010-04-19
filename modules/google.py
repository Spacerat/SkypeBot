
import interface
import urllib2
import json
from stringsafety import *

def Handle(interface,command,args,messagetype):
    # @type args str
    showcontent = (command!='googleurl')
    showurl = (command!='googlecontent')

    url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&gl=uk&q="+escapeurl(args,plus=True)
    request = urllib2.Request(url,None,{'Referer':'http://spacerat.meteornet.net'})
    response = urllib2.urlopen(request)
    results = json.load(response)
    if results["responseData"]["results"]:
        for result in results["responseData"]["results"]:
            if 'youtube' in result["url"]: continue
            if showurl==True: interface.Reply(result["url"])
            content = result["content"]
            if showcontent==True: interface.Reply(FormatHTML(content))
            break
    else:
        interface.Reply("No results for "+args+"!")

def Translate(interface,command,args,messagetype):
    c = args.partition(" ")
    lang=c[0]
    if "|" not in lang:
        lang="en|"+lang
    url = "http://ajax.googleapis.com/ajax/services/language/translate?v=1.0&q="+escapeurl(c[2])+"&langpair="+escapeurl(lang)
    request = urllib2.Request(url,None,{'Referer':'http://spacerat.meteornet.net'})
    response = urllib2.urlopen(request)
    results = json.load(response)

    if results['responseStatus']!=200:
        interface.Reply(results['responseDetails'])
    else:
        interface.Reply(results["responseData"]["translatedText"])

interface.AddHook("google",Handle,name="GoogleBot")
interface.AddHook("googleurl",Handle,name="GoogleBot")
interface.AddHook("googlecontent",Handle,name="GoogleBot")
interface.AddHook("translate",Translate,name="GoogleBot")