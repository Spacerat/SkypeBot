
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

    def Reply(self, text,edit=False):
        outp = unicode(text)
        if self.Name<>"": outp=unicode(self.Name)+": "+outp
        if edit and self.Message.IsEditable:
            self.Message.Body=outp
        else:
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
    @property
    def UserAddress(self):
        return self.Message.Sender.Handle
