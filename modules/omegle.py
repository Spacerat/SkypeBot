
import interface
import omeglelib
import threading
import urllib2
from time import sleep

class Omg(threading.Thread):
    chats = {}

    def __init__(self,interface,named):
        threading.Thread.__init__(self)
        self.i = interface
        self.named = named
    def run(self):
        if self.i.ChatName in Omg.chats.keys():
            self.i.Reply("~An Omegle chat is already going on in this conversation!")
            return

        c = omeglelib.OmegleChat()
        self.chat=c
        self.chat.named = self.named
        Omg.chats[self.i.ChatName] = self
        c.connect_events(SkypeMeggleEvents(self.i))
        #c.debug=True
        try:
            c.connect(False)
        except urllib2.URLError, e:
            self.i.Reply("~Error while connecting!")
            self.i.Reply("~%s"%str(e))
            c.disconnect()


    def say(self,text,name):
        try:
            if self.named == True:
                self.chat.say("%s: %s"%(name[:3],text))
            else:
                self.chat.say(text)
        except urllib2.HTTPError, e:
            self.i.Reply("~%u Error while sending %s" %(e.code,text))
            

class SkypeMeggleEvents(omeglelib.EventHandler):

    def __init__(self,interface):
        self.i = interface

    def connected(self,chat,var):
        self.i.Reply("~OmegleBot: New chat started!")
        self.i.Reply("~Prefix messages with ~ to omit them from the omegle conversation.")
        
        if chat.named:
            sleep(1)
            chat.say("Hi there! You're currently talking to a room full of different people.")
        chat.in_chat = True
        #chat.say("Hello!")

    def gotMessage(self,chat,message):
        message = message[0]
        self.i.Reply("~Stranger: "+message)

    def typing(self,chat,var):
        print "Stranger is typing..."

    def stoppedTyping(self,chat,var):
        print "Stranger stopped typing!"

    def strangerDisconnected(self,chat,var):
        
        self.i.Reply("~OmegleBot: Stranger left.")
        chat.terminate()

    def terminate(self,chat,var):
        self.i.Reply("~Terminating OmegleBot.")
        del Omg.chats[self.i.ChatName]

def StartOmegle(i,command,args,messagetype):
    """!omegle <anon|named> - Starts an omegle session. You must specify either anonymous or named mode. 
    In anon, Stranger cannot distinguish between skype users. In named mode, The first three letters of your nickname are prepended to your message.
    Use !endomegle to end the session."""
    if args=='anon':
        Omg(i,False).start()
    elif args=='named':
        o = Omg(i,True)
        o.start()
    else:
        interface.Name = "Help"
        interface.HelpHandle(i,'help',command,messagetype)


def EndOmegle(interface,command,args,messagetype):
    """!endomegle - Ends an omegle session running in this channel."""
    try:
        c = Omg.chats[interface.ChatName]
        c.chat.disconnect()
    except:
        interface.Reply("There is no omegle session currently running in this conversation.")


def Handle(interface,text):
    if not hasattr(Omg,'chats'):
        Omg.Chats = {}
    c = Omg.chats.get(interface.ChatName,None)
    if not c: return
    if text.startswith("~"): return
    if c.chat.terminated: return
    c.say(text,interface.UserName)

def terminate():
    print "Terminating chats."
    for c in Omg.chats.itervalues():
        c.chat.disconnect()
    Omg.chats={}
    

interface.MessageHook(Handle)
interface.ComHook("omegle",StartOmegle)
interface.ComHook("endomegle",EndOmegle)