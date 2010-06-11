
from interface import ChatInterface
import math

class SkypeInterface(ChatInterface):

    skype=None

    def __init__(self, Message, MessageStatus):
        self.Message = Message
        self.MessageStatus = MessageStatus
        self.OnInit()

    def OnInit(self):
        self.Name=''

    def Reply(self, text,edit=False):
        outp=text
        if not isinstance(text,unicode):
            try:
                outp = unicode(text,errors='ignore')
            except:
                outp = str(text)
        if self.Name<>"": outp=unicode(self.Name)+": "+outp
        if edit and self.Message.IsEditable:
            self.Message.Body=outp
        else:
            self.Message.Chat.SendMessage(outp)

    def SetTopic(self,topic):
        try:
            self.Message.Chat.Topic=topic
        except:
            pass

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

    @property
    def UserName(self):
        return self.Message.Sender.FullName
