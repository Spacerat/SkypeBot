
import robot
import urllib2
from stringsafety import *
from xml.dom import minidom

def SetToken(str):
    global tokenstr
    token = str
    tokenstr = "tokenid="+token

tokenstr=''

class DefineRobot(robot.SkypeRobot):
    def OnInit(self):
        self.Name = "DefineBot"
    def Handle(self,command,args):
        # @type args str
        url = "http://www.abbreviations.com/services/v1/"
        if command=='define':
            url+='syno.aspx?'+tokenstr+'&word='+URLSafe(args)
        else: 
            url+='abbr.aspx?'+tokenstr+'&categoryid=Chat&term='+URLSafe(args)
        request = urllib2.Request(url,None,{'Referer':'http://spacerat.meteornet.net'})
        response = urllib2.urlopen(request)
        #for x in response.readlines():
        #    print x
        data = minidom.parse(response)

        # @type data Document
        for top in data.childNodes:
            if top.childNodes:
                result = top.childNodes[0]
                defin = result.getElementsByTagName("definition")[0].firstChild.data.capitalize()+"."
                term = string.capwords(result.getElementsByTagName("term")[0].firstChild.data)

                if command=='define':
                    part = result.getElementsByTagName("partofspeach")[0].firstChild.data
                    self.Reply("http://www.definitions.net/definition/"+URLSafe(args))
                    self.Reply("{0} ({1})".format(term,part))
                    self.Reply(defin)
                elif command=='abbr':
                    cat = result.getElementsByTagName("category")[0].firstChild.data
                    self.Reply("http://www.abbreviations.com/"+URLSafe(args))
                    self.Reply("{0} ({1})".format(term,cat))
                    self.Reply(defin)

robot.AddHook("define",DefineRobot)
robot.AddHook("abbr",DefineRobot)

