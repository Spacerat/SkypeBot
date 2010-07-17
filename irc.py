import sys
import socket
import string
from modules.interface import RecieveMessage, ChatInterface
from modules.ircinterface import IRCInterface
import threading

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

