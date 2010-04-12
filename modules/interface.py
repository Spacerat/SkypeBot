
Hooks = {}
Names = {}

def AddHook(command,hook,name):
    Hooks[command]=hook
    Names[command] = name

def RecieveMessage(Interface,text,MessageStatus):
    if MessageStatus == 'SENT' or MessageStatus == 'RECEIVED' and text!='':
        if (text[0]=="!"):
            command =  text.partition(" ")[0][1:len(text)]
            body = text.partition(" ")[2]
            if command in Hooks:
                Interface.Name = Names[command]
                hook = Hooks[command]
                hook(Interface,command,body,MessageStatus)

def GetCommands(interface,command='',args='',MessageStatus=''):
    output=''
    for key in Hooks.iterkeys():
        output+="!"+key+"  "
    interface.Reply(output)

class ChatInterface:
    def Reply(self, text): pass

AddHook('commands',GetCommands,'CommandBot: ')