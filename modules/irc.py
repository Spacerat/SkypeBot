
import sys
import socket
import string
from interface import RecieveMessage, ChatInterface, ComHook
import threading


class IRCInterface(ChatInterface):

    skype=None

    def __init__(self, irc,channel, Message,nick="",host=""):
        self.irc = irc
        self.channel = channel
        self.nick=nick
        self.host=host
        self.BotHandle = irc.network.nick
        self.OnInit()

    def OnInit(self):
        self.Name='IRCRobot'

    def Reply(self, text,edit=False):
        self.irc.msg(self.channel,text)

    def SetTopic(self,topic):
        self.irc.SetTopic(self.channel,topic)

    @property
    def LastMessages(self):
        pass

    @property
    def UserAddress(self):
        return self.host

    @property
    def UserName(self):
        return self.nick

    @property
    def Type(self):
        return 'IRC'

    @property
    def ChatName(self):
        return self.channel

class IRC(threading.Thread):
    def __init__(self,network):
        self.network = network
        self.connected = False
        threading.Thread.__init__(self)

    def run(self):
        print "IRC Starting."
        self.sock = socket.socket()
        self.sock.connect((self.network.server,self.network.port))
        self.send("NICK %s\r\n" % self.network.nick)
        self.send("USER %s 8 *: %s" % (self.network.ident, self.network.realname))
        self.send("PONG")
        self.connected = True

        readbuffer=""
        while self.connected:
            readbuffer=readbuffer+self.sock.recv(1024)
            temp=string.split(readbuffer, "\n")
            readbuffer=temp.pop( )

            for line in temp:
                line=string.rstrip(line)
                cmd=''
                nick=''
                host=''
                if line[0]==":":
                    hostmask, line = line[1:].split(' ',1)
                    if "!" in hostmask:
                        nick = hostmask.split("!")[0]
                        host = hostmask.split("!")[1]
                    else:
                        host=hostmask
                else:
                    pass

                parts = line.split(' :',1)
                args = parts[0].split()
                cmd=args[0]

                if cmd=="PING":
                    self.send("PONG %s" % parts[1])
                elif cmd=="MODE":
                    for s in self.network.channels:
                        self.send("JOIN %s" % s)
                elif cmd=="PRIVMSG":
                    message=parts[1]
                    channel=args[1]
                    #print nick,host,message
                    #try:
                    threading.Thread(None, RecieveMessage, None,[IRCInterface(self,channel,message,nick=nick,host=host),message,'RECEIVED']).start()
                    #RecieveMessage()
                    #except Exception as e:
                    #    print str(e)


    def send(self, str):
        #Lock is a good idea. Do that at some point.
#        print "OUTPUT:", "%s\r\n" % str
        self.sock.send(("%s\r\n" % str).encode('utf-8','ignore'))

    def msg(self,channel,message):
        self.send("PRIVMSG "+channel+" :"+message)

    def SetTopic(self,channel,topic):
        self.send("TOPIC "+channel+" :"+topic)

    def disconnect(self, reason=""):
        self.send("QUIT :"+reason)

#Yoink. Thanks Katharine.
class Network:
    server = ''
    port = 6667
    nicks = ()
    realname = ''
    ident = ''
    primary_channel = None
    name = ''
    password = None

    def __init__(self, server='', port=6667, nick=None, realname='', ident='', channels=None, name='', password=None):
        self.server = server
        self.port = port
        self.nick = nick
        self.realname = realname
        self.ident = ident
        self.channels = channels
        self.name = name
        self.password = password

    def __str__(self):
        return self.name


def StartIRC(i=None,command=None,args=None,messagetype=None):
    """!irc network channel - Connect to an irc network/channel."""
    args=args.split()
    if len(args)!=2:
        modules.interface.HelpHandle(interface, 'help','irc',messagetype)
        return

    IRC(Network(server=args[0],nick='SpaceBot',ident='spacebot',realname="SpaceBot",channels=[args[1]] )).start()

ComHook('irc',StartIRC,security=4,name='ChatBot')
