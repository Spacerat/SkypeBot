class SkypeRobot:
    def __init__(self, Message, MessageStatus):
        self.Message = Message
        self.MessageStatus = MessageStatus

    def Reply(self, text):
        self.Message.Chat.SendMessage(text)

    def ToString(self):
        return "SkypeBotModule"

    def Handle(self,command,args): pass


print "defined SkypeRobot"
