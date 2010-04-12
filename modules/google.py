
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
        if showurl==True: interface.Reply(results["responseData"]["results"][0]["url"])
        content = results["responseData"]["results"][0]["content"]
        if showcontent==True: interface.Reply(FormatHTML(content))
    else:
        interface.Reply("No results for "+args+"!")

        
interface.AddHook("google",Handle,"GoogleBot")
interface.AddHook("googleurl",Handle,"GoogleBot")
interface.AddHook("googlecontent",Handle,"GoogleBot")