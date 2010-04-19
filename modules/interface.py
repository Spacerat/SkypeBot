
class MessageHook:

    Hooks = []

    def __init__(self,hook):
        self.Hook = hook
        MessageHook.Hooks.append(self)

class ComHook:

    Hooks = {}

    def __init__(self,command,hook,name='',status='ANY',prefix="!"):
        self.Name = name
        self.MStatus = status
        self.Hook = hook
        self.prefix="!"
        ComHook.Hooks[command]=self


#This function is now essentially redundant. Yay!
def AddHook(command,hook,name='',status='ANY'):
    ComHook(command,hook,name=name,status=status)

def RecieveMessage(Interface,text,MessageStatus):

    if text!="":
        command =  text.partition(" ")[0][1:len(text)]
        body = text.partition(" ")[2]
        
        #Super hooks
        if (MessageStatus =='SENT' or MessageStatus == 'RECEIVED'):
            for hook in MessageHook.Hooks:
                hook.Hook(Interface,text)

        #Command hooks
        if command in ComHook.Hooks:
            mtype = ComHook.Hooks[command].MStatus
            if ((mtype=='ANY' and (MessageStatus =='SENT' or MessageStatus == 'RECEIVED')) or MessageStatus == mtype) and text.startswith(ComHook.Hooks[command].prefix):
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
    @property
    def LastMessages(self): pass


ComHook('commands',GetCommands,name='CommandBot')
