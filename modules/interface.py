
class MessageHook:

    Hooks = []

    def __init__(self,hook):
        self.Hook = hook
        MessageHook.Hooks.append(self)

class ComHook:

    Hooks = {}

    def __init__(self,command,hook,name='',status='ANY',hidden=False):
        self.Name = name
        self.MStatus = status
        self.Hook = hook
        self.Hidden = hidden
        ComHook.Hooks[command]=self


#This function is now essentially redundant. Yay!
def AddHook(command,hook,name='',status='ANY'):
    ComHook(command,hook,name=name,status=status)

def RecieveMessage(Interface,text,MessageStatus):

    if text!="":
        command =  text.partition(" ")[0][len(Interface.Prefix):len(text)].lower()
        body = text.partition(" ")[2]
        
        #Super hooks
        if (MessageStatus =='SENT' or MessageStatus == 'RECEIVED'):
            for hook in MessageHook.Hooks:
                hook.Hook(Interface,text)

        #Command hooks
        if command in ComHook.Hooks:
            mtype = ComHook.Hooks[command].MStatus
            if ((mtype=='ANY' and (MessageStatus =='SENT' or MessageStatus == 'RECEIVED')) or MessageStatus == mtype) and text.startswith(Interface.Prefix):
                Interface.Name = ComHook.Hooks[command].Name
                hook = ComHook.Hooks[command].Hook
                hook(Interface,command,body,MessageStatus)

def SetPrefix(prefix,overwrite=False):
    try:
        if ChatInterface.Prefix!="" and overwrite==False: return
    except:
        pass
    ChatInterface.Prefix=prefix

def GetPrefix():
    return ChatInterface.Prefix


def GetCommandsHandle(interface,command='',args='',MessageStatus=''):
    """!commands - Get a list of commands."""
    output=''
    for key in ComHook.Hooks.iterkeys():
        if ComHook.Hooks[key].Hidden == False: output+=interface.Prefix+key+"  "
    interface.ReplyToSender(output)

def HelpHandle(interface,command='',args='',MessageStats=''):
    """!help command - Get help for a particular command."""
    if args.strip=="":
        interface.Reply("!help command, gets help for a particular command. Type !commands to see a list of every commands.")
    else:
        try:
            hook = ComHook.Hooks[args]
        except:
            interface.Reply("No help stored for "+args)
            return
        func = hook.Hook
        interface.Reply(func.__doc__.replace("!",GetPrefix()))

def SetPrefixHandle(interface,command='',args='',MessageStatus=''):
    ChatInterface.Prefix=args

def Ping(interface,command='',args='',MessageStatus=''):
    """!ping - PONG"""
    interface.Reply("PONG!")

def Marco(interface,command='',args='',MessageStatus=''):
    """!marco - POLO"""
    interface.Reply("POLO!")

class ChatInterface:

    Prefix=''

    def Reply(self, text, edit=False): pass
    def ReplyToSender(self, text):
        self.Reply(text)
    @property
    def LastMessages(self): pass
    @property
    def UserName(self): pass
    @property
    def UserAddress(self): pass
    @property
    def Type(self):
        return 'Null'
    @property
    def IsEditable(self):
        return False
    def GetPrefix(self):
        return ChatInterface.Prefix

class DebugInterface(ChatInterface):
    def Reply(self,text,edit=False):
        print text

ComHook('commands',GetCommandsHandle,name='CommandBot')
ComHook('help',HelpHandle,name='Help')
ComHook('prefix',SetPrefixHandle,hidden=True)
ComHook('ping',Ping)
ComHook('marco',Marco)
