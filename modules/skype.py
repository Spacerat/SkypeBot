
from interface import ChatInterface
import math

class SkypeInterface(ChatInterface):

    skype=None

    def __init__(self, Message, MessageStatus, Skype):
        self.Message = Message
        self.MessageStatus = MessageStatus
        self.Skype = Skype
        self.OnInit()

    def OnInit(self):
        self.Name=''

    def _sanitisetext(self,text):
        outp=text
        if not isinstance(text,unicode):
            try:
                outp = unicode(text,errors='ignore')
            except:
                outp = str(text)
        if self.Name<>"": outp=unicode(self.Name)+": "+outp
        return outp

    def Reply(self, text,edit=False):
        outp=self._sanitisetext(text)

        if edit and self.Message.IsEditable:
            self.Message.Body=outp
        else:
            self.Message.Chat.SendMessage(outp)

    def ReplyToSender(self,text):
        if self.MessageStatus=="SENT":
            self.Reply(text)
            return
        outp=self._sanitisetext(text)

        self.Skype.SendMessage(self.UserAddress,outp)


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
        return self.Message.FromHandle

    @property
    def UserName(self):
        return self.Message.FromDisplayName

    @property
    def Users(self):
        r = {}
        for u in self.Message.Chat.Members:
            r[u.FullName]= u.Handle
            
        return r
    @property
    def Type(self):
        return "Skype"
