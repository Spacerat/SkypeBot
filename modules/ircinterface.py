
from interface import ChatInterface

class IRCInterface(ChatInterface):

    skype=None

    def __init__(self, irc,channel, Message,nick="",host=""):
        self.irc = irc
        self.channel = channel
        self.nick=nick
        self.host=host
        self.OnInit()

    def OnInit(self):
        self.Name='IRCRobot'

    def Reply(self, text,edit=False):
        self.irc.msg(self.channel,text)

    def SetTopic(self,topic):
        self.irc.SetTopic(self.channel,topic)

    @property
    def LastMessages(self):
        pass

    @property
    def UserAddress(self):
        return self.host

    @property
    def UserName(self):
        return self.nick
