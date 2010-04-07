
import robot
import urllib2
import json
from stringsafety import *

class GoogleRobot(robot.SkypeRobot):
    def OnInit(self):
        self.Name = "GoogleBot"
    def Handle(self,command,args):
        # @type args str
        url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q="+URLSafe(args)
        request = urllib2.Request(url,None,{'Referer':'http://spacerat.meteornet.net'})
        response = urllib2.urlopen(request)
        results = json.load(response)
        self.Reply(results["responseData"]["results"][0]["url"])
        content = results["responseData"]["results"][0]["content"]        
        self.Reply(FormatHTML(content))

robot.AddHook("google",GoogleRobot)

