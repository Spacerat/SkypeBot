
class ComHook:

    Hooks = {}

    def __init__(self,command,hook,name='',status='ANY'):
        self.Name = name
        self.MStatus = status
        self.Hook = hook
        ComHook.Hooks[command]=self

#This function is now essentially redundant. Yay!
def AddHook(command,hook,name='',status='ANY'):
    ComHook(command,hook,name=name,status=status)

def RecieveMessage(Interface,text,MessageStatus):

    if text!="" and (text[0]=="!"):
        command =  text.partition(" ")[0][1:len(text)]
        body = text.partition(" ")[2]
        if command in ComHook.Hooks:
            mtype = ComHook.Hooks[command].MStatus
            if (mtype=='ANY' and (MessageStatus =='SENT' or MessageStatus == 'RECEIVED')) or MessageStatus == mtype:
                Interface.Name = ComHook.Hooks[command].Name
                hook = ComHook.Hooks[command].Hook
                hook(Interface,command,body,MessageStatus)

def GetCommands(interface,command='',args='',MessageStatus=''):
    output=''
    for key in ComHook.Hooks.iterkeys():
        output+="!"+key+"  "
    interface.Reply(output)

class ChatInterface:
    def Reply(self, text): pass
    def LastMessages(self,num=10): pass


ComHook('commands',GetCommands,name='CommandBot')
