
import msnlib
import msncb
import threading
import select
import socket
from modules.interface import RecieveMessage, ChatInterface, ComHook

class MSNInterface(ChatInterface):

    skype=None

    def __init__(self, msn, Message, email):
        self.msn = msn
        self.Message = Message
        self.email = email
        self.OnInit()

    def OnInit(self):
        self.Name='MSNRobot'

    def Reply(self, text,edit=False):
        outp=text
        '''
        if not isinstance(text,unicode):
            try:
                outp = unicode(text,errors='ignore')
            except:
                outp = str(text)
        '''
        if self.Name<>"": outp=unicode(self.Name)+": "+outp
        self.msn.sendmsg(self.email,outp)
        #print self.email
    @property
    def LastMessages(self):
        pass
    @property
    def UserAddress(self):
        #return self.Message.Sender.Handle
        pass
    @property
    def Type(self):
        return "MSN"

def recvmsg(md, type, tid, params, sbd):
	t = tid.split()
	email = t[0]

	if email == 'Hotmail':
		return

	lines = params.split('\n')
	headers = {}
	eoh = 1
	for i in lines:
		if i == '\r':
			break
		t, v = i.split(':', 1)
		headers[t] = v
		eoh += 1

	if headers.get('Content-Type', '') == 'text/x-msmsgscontrol':
		# typing, ignore
		return

        line = lines[eoh].strip()
        if (line):
            try:
                threading.Thread(None,RecieveMessage( MSNInterface(md,line,email),line,'RECEIVED' ))
            except:
                pass
            #md.sendmsg(email, line)


	#msncb.cb_msg(md, type, tid, params, sbd)

msn = msnlib.msnd()
msn.cb = msncb.cb()
msn.cb.msg = recvmsg

def init():

    global msn

    ChatInterface.Prefix = "!"
    data = open("data/msndata.txt").readlines()
    msn.email=data[0][0:len(data[0])-1]
    msn.pwd=data[1]

    msn.login()

    msn.sync()
    msn.change_status("online")

    # we loop over the network socket to get events
    print "Loop"
    while 1:
            # we get pollable fds
            t = msn.pollable()
            infd = t[0]
            outfd = t[1]

            # we select, waiting for events
            try:
                    fds = select.select(infd, outfd, [])
            except:
                    quit()

            for i in fds[0] + fds[1]:       # see msnlib.msnd.pollable.__doc__
                    try:
                            msn.read(i)
                    except ('SocketError', socket.error), err:
                            if i != msn:
                                    # user closed a connection
                                    # note that messages can be lost here
                                    msn.close(i)
                            else:
                                    # main socket closed
                                    quit()

def StartMSN(i=None,command=None,args=None,messagetype=None):
    """!startmsn - Start the msn bot"""
    threading.Thread(None,init).start()

ComHook('msn',StartMSN,security=4,name="ChatBot")