Hooks = {}

def RecieveMessage(Message,MessageStatus):
    text = Message.Body

    if MessageStatus == 'SENT' or MessageStatus == 'RECEIVED':
        if (text[0]=="!"):
            command =  text.partition(" ")[0][1:len(text)]
            body = text.partition(" ")[2]
            if command in Hooks:
                rob = Hooks[command](Message,MessageStatus)
                rob.Handle(command,body)

def AddHook(name,robotclass):
    Hooks[name]=robotclass

class SkypeRobot:
    def __init__(self, Message, MessageStatus):
        self.Message = Message
        self.MessageStatus = MessageStatus
        self.OnInit()

    def OnInit(self):
        self.Name='SkypeRobot'

    def Reply(self, text):
        self.Message.Chat.SendMessage(self.Name+": "+text)

    def ToString(self):
        return "SkypeBotModule"

    def Handle(self,command,args):
        if command=='commands':
            output=''
            for key in Hooks.iterkeys():
                output+="!"+key+"  "
            self.Reply(output)

AddHook('commands',SkypeRobot)
