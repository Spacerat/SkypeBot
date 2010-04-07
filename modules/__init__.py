
import Skype4Py

Hooks = {}

print "init hooks"

def RecieveMessage(Message,MessageStatus):
    text = Message.Body

    if MessageStatus == 'SENT' or MessageStatus == 'RECEIVED':
        if (text[0]=="!"):
            command =  text.partition(" ")[0][1:len(text)]
            body = text.partition(" ")[2]
            rob = Hooks[command](Message,MessageStatus)
            rob.Handle(command,body)