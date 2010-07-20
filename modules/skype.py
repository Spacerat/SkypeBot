
from interface import ChatInterface
from interface import ComHook
import math
import Skype4Py
from interface import RecieveMessage

skype = Skype4Py.Skype()

# ----------------------------------------------------------------------------------------------------
# Fired on attachment status change. Here used to re-attach this script to Skype in case attachment is lost. Just in case.
def OnAttach(status):
    print 'API attachment status: ' + skype.Convert.AttachmentStatusToText(status)
    if status == Skype4Py.apiAttachAvailable:
        skype.Attach();

    if status == Skype4Py.apiAttachSuccess:
       print('******************************************************************************');

# ----------------------------------------------------------------------------------------------------
# Fired on chat message status change.
# Statuses can be: 'UNKNOWN' 'SENDING' 'SENT' 'RECEIVED' 'READ'

def OnMessageStatus(Message, Status):
    RecieveMessage( SkypeInterface(Message,Status,skype),Message.Body,Status )

# ----------------------------------------------------------------------------------------------------
# Creating instance of Skype object, assigning handler functions and attaching to Skype.

def Init():

    skype.OnAttachmentStatus = OnAttach;
    skype.OnMessageStatus = OnMessageStatus;

    print('******************************************************************************');
    print 'Connecting to Skype..'
    skype.Attach()

def StartSkype(i=None,command=None,args=None,messagetype=None):
    """!skype - Start the skype bot"""
    Init()

class SkypeInterface(ChatInterface):

    skype=None

    def __init__(self, Message, MessageStatus, Skype):
        self.Message = Message
        self.MessageStatus = MessageStatus
        self.Skype = Skype
        self.BotHandle = Skype.CurrentUser.Handle
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
    def IsEditable(self):
        return self.Message.IsEditable

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

    @property
    def ChatName(self):
        return self.Message.ChatName

SkypeInterface.skype = skype

ComHook('skype',StartSkype,security=4,name="ChatBot")