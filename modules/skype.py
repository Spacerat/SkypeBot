
from interface import ChatInterface
import math

class SkypeInterface(ChatInterface):

    skype=None

    def __init__(self, Message, MessageStatus):
        self.Message = Message
        self.MessageStatus = MessageStatus
        self.OnInit()

    def OnInit(self):
        self.Name='SkypeRobot'

    def Reply(self, text):
        outp = text
        if self.Name<>"": outp=self.Name+": "+unicode(text)
        self.Message.Chat.SendMessage(outp)

    @property
    def LastMessages(self):
        messages = self.Message.Chat.RecentMessages
        ret = []
        try:
            for x in range(0,20):
                ret.append(messages[len(messages)-2-x])
        except IndexError:
            pass
        
        return ret
