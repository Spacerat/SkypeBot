
import skrobot
import urllib2
import json
import re

class WikiRobot(skrobot.SkypeRobot):
    def OnInit(self):
        self.Name = "WikiBot"
    def Handle(self,command,args):
        # @type args str
        args = args.replace(" ","%20")

        url = "http://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=json&titles="+args
        request = urllib2.Request(url,None,{'Referer':'http://spacerat.meteornet.net'})
        response = urllib2.urlopen(request)
        results = json.load(response)
        if results:
            if "pages" in results["query"]:
                for page in results["query"]["pages"]:
                    if "revisions" in results["query"]["pages"][page]:
                        p = re.compile(r'(\{\{).*?(\}\})<.*?>')
                        text = results["query"]["pages"][page]["revisions"][0]['*']
                        text = text.replace(chr(10),"")
                        text = p.sub('',text)
                        if text.startswith("#REDIRECT"):
                            rd = re.compile(r'(#REDIRECT)*(\[)*(\])*')

                            text = rd.sub('',text)
                            self.Handle(command,text)
                        else:
                            rf = re.compile(r"(\[)*(\])*(')*")
                            text = rf.sub('',text)
                            self.Reply( text.encode('utf-8')[0:400]+" ...")
                     #   self.Reply(results["query"]["pages"][page]["revisions"][0]['*'].encode('utf-8').partition(chr(10))[0])
            else:
                self.Reply("Wikipedia page for "+args+" does not exit.")
        else:
         print "no results"

robot.AddHook("wiki",WikiRobot)

