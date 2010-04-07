
import robot
import urllib2
import json
import codecs

class GoogleRobot(robot.SkypeRobot):
    def OnInit(self):
        self.Name = "GoogleBot"
    def Handle(self,command,args):
        # @type args str
        args = args.replace(" ","%20")
        
        url = "http://ajax.googleapis.com/ajax/services/search/web?v=1.0&q="+args
        request = urllib2.Request(url,None,{'Referer':'http://spacerat.meteornet.net'})
        response = urllib2.urlopen(request)
        results = json.load(response)
        self.Reply(results["responseData"]["results"][0]["url"])
        self.Reply(results["responseData"]["results"][0]["content"])

robot.AddHook("google",GoogleRobot)

