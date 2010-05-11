
from interface import ChatInterface
import math

class MSNInterface(ChatInterface):

    skype=None

    def __init__(self, msn, line, email):
        self.msn = msn
        self.line = line
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
        print outp
    @property
    def LastMessages(self):
        pass
    @property
    def UserAddress(self):
        #return self.Message.Sender.Handle
        pass
