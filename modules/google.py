
import interface
import urllib2
import json
from stringsafety import *

def Handle(interface,command,args,messagetype):
    """(!g, !google, !googleurl, !googlecontent) search_string - Googles search.
    !g and !google return a url and content. !googlecontent and !googleurl return one or the other.
    """

    if args.strip()=="":
        interface.Reply("Use %s%s phrase" %(interface.GetPrefix(),command))
        return
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
    """(!translate, !translateme) language phrase - translate phrase in to language (such as en, fr, de).
    Language can be two languages, e.g. fr|en or de|fr."""
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
        interface.Reply(results["responseData"]["translatedText"],edit=(command=='translateme'))

interface.ComHook("g",Handle,name="GoogleBot")
interface.ComHook("google",Handle,name="GoogleBot")
interface.ComHook("googleurl",Handle,name="GoogleBot")
interface.ComHook("googlecontent",Handle,name="GoogleBot")
interface.ComHook("translate",Translate,name="GoogleBot")
interface.ComHook("translateme",Translate,name="GoogleBot")
