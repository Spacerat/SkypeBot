
from interface import ChatInterface

class SkypeInterface(ChatInterface):
    def __init__(self, Message, MessageStatus):
        self.Message = Message
        self.MessageStatus = MessageStatus
        self.OnInit()

    def OnInit(self):
        self.Name='SkypeRobot'

    def Reply(self, text):
        outp = text
        if self.Name<>"": outp=self.Name+": "+text
        self.Message.Chat.SendMessage(outp)
