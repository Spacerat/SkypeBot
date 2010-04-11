
import interface
import urllib2
import json
from stringsafety import *

def Handle(interface,command,args,messagetype):
    # @type args str
    args = args.replace(' ','+')
    url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&gl=uk&q="+args
    request = urllib2.Request(url,None,{'Referer':'http://spacerat.meteornet.net'})
    response = urllib2.urlopen(request)
    results = json.load(response)
    if results["responseData"]["results"]:
        interface.Reply(results["responseData"]["results"][0]["url"])
        content = results["responseData"]["results"][0]["content"]
        interface.Reply(FormatHTML(content))
    else:
        interface.Reply("No results for "+URLSafe(args)+"!")

        
interface.AddHook("google",Handle,"GoogleBot")
