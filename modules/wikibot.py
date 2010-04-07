# 

import robot
import urllib2
import json

class WikiRobot(robot.SkypeRobot):
    def OnInit(self):
        self.Name = "WikiBot"
    def Handle(self,command,args):
        # @type args str
        args = args.replace(" ","%20")

        url = "http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&titles="+args
        request = urllib2.Request(url,None,{'Referer':'http://spacerat.meteornet.net'})
        response = urllib2.urlopen(request)
        results = json.load(response)
        if "pages" in results["query"]:
            for page in results["query"]["pages"]:
                self.Reply(results["query"]["pages"][page]["revisions"][0]['*'].encode('utf-8').partition(chr(10))[0])
        else:
            self.Reply("Wikipedia page for "+args+" does not exit.")
robot.AddHook("wiki",WikiRobot)

