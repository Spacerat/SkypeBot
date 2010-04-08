
import skrobot
import urllib2
import json
from stringsafety import *

class GoogleRobot(skrobot.SkypeRobot):
    def OnInit(self):
        self.Name = "GoogleBot"
    def Handle(self,command,args):
        # @type args str
        args = args.replace(' ','+')
        url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q="+args
        request = urllib2.Request(url,None,{'Referer':'http://spacerat.meteornet.net'})
        response = urllib2.urlopen(request)
        results = json.load(response)
        if results["responseData"]["results"]:
            self.Reply(results["responseData"]["results"][0]["url"])
            content = results["responseData"]["results"][0]["content"]
            self.Reply(FormatHTML(content))
        else:
            self.Reply("No results for "+URLSafe(args)+"!")
skrobot.AddHook("google",GoogleRobot)

