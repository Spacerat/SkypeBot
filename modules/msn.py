
from interface import ChatInterface
import math

class MSNInterface(ChatInterface):

    skype=None

    def __init__(self, msn, Message, email):
        self.msn = msn
        self.Message = Message
        self.email = email
        self.OnInit()

    def OnInit(self):
        self.Name='MSNRobot'

    def Reply(self, text,edit=False):
        outp=text
        '''
        if not isinstance(text,unicode):
            try:
                outp = unicode(text,errors='ignore')
            except:
                outp = str(text)
        '''
        if self.Name<>"": outp=unicode(self.Name)+": "+outp
        self.msn.sendmsg(self.email,outp)
        #print self.email
    @property
    def LastMessages(self):
        pass
    @property
    def UserAddress(self):
        #return self.Message.Sender.Handle
        pass
    @property
    def Type(self):
        return "MSN"