import security
import modules
import inspect
from modules import *

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
                c = ComHook.Hooks[command]
                Interface.Name = c.Name
                if security.GetSecurityForHandle(Interface,Interface.UserAddress)<c.Security:
                    Interface.Reply("Use of this command requires an access level of %u"%c.Security)
                elif c.Admin == True and security.GetAdminForHandle(Interface,Interface.UserAddress)==False:
                    Interface.Reply("You must have admin access in this conversation to use this command.")
                else:
                    c.Hook(Interface,command,body,mtype)

def SetPrefix(prefix,overwrite=False):
    try:
        if ChatInterface.Prefix!="" and overwrite==False: return
    except:
        pass
    ChatInterface.Prefix=prefix

def GetPrefix():
    return ChatInterface.Prefix

##################################
#######   CORE COMMANDS   ########
##################################

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
            func = hook.Hook
            interface.Reply(func.__doc__.replace("!",GetPrefix()),edit=True)
            interface.Reply("Access: %u  Admin: %s"%(hook.Security,hook.Admin))
        except:
            interface.Reply("No help stored for "+args)
            return
        

def SetPrefixHandle(interface,command='',args='',MessageStatus=''):
    ChatInterface.Prefix=args

def Ping(interface,command='',args='',MessageStatus=''):
    """!ping - PONG"""
    interface.Reply("PONG!")

def Marco(interface,command='',args='',MessageStatus=''):
    """!marco - POLO"""
    interface.Reply("POLO!")

def LoadMod(interface,command,args,MessageStatus):
    """!load modname - Load a module."""
    try:
        add_module(args)
        interface.Reply("Loaded %s"%args)
    except ImportError, e:
        interface.Reply(str(e))
    except ModuleAlreadyLoaded, e:
        interface.Reply(str(e))

def UnloadMod(interface,command,args,MessageStatus):
    """!unload modname - Unload a module."""
    try:
        unload_module(args)
        interface.Reply("Unloaded %s"%args)
    except Exception as e:
        interface.Reply(str(e))

class ChatInterface:

    Prefix='!'

    def Reply(self, text, edit=False): pass
    def ReplyToSender(self, text):self.Reply(text)
    @property
    def LastMessages(self): pass
    @property
    def UserName(self): pass
    @property
    def UserAddress(self): pass
    @property
    def Type(self):return 'Null'
    @property
    def IsEditable(self): return False
    @property
    def ChatName(self): pass
    @property
    def BotNick(self): pass
    @property
    def BotHandle(self): pass
    def GetPrefix(self):
        return ChatInterface.Prefix



class DebugInterface(ChatInterface):

    def __init__(self):
        self.Name="Console"

    def Reply(self, text,edit=False):
        outp = text
        if self.Name<>"": outp=self.Name+": "+outp
        #outp = unicode(outp,errors='ignore')
        print outp.encode('ascii','ignore')
    @property
    def UserName(self):
        return "Console"
    @property
    def UserAddress(self):
        return "Console"
    @property
    def Type(self):
        return "Console"
    @property
    def ChatName(self):
        return "Console"
    @property
    def BotNick(self):
        return "Console"
    @property
    def BotHandle(self):
        return "Console"

ComHook('commands',GetCommandsHandle,name='CommandBot')
ComHook('help',HelpHandle,name='Help')
ComHook('prefix',SetPrefixHandle,security=3)
ComHook('ping',Ping)
ComHook('marco',Marco)
ComHook('load',LoadMod,security=4,name='ChatBot')
ComHook('unload',UnloadMod,security=4,name='ChatBot')