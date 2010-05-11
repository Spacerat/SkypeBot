# ----------------------------------------------------------------------------------------------------
#  Python / Skype4Py super Skype Bot

import msnlib
import msncb
import threading
import time
import select
import socket
from modules.interface import RecieveMessage, ChatInterface
from modules.msn import MSNInterface

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


'''
if __name__ == "__main__":
    Cmd = '';
    while not Cmd == 'exit':
        Cmd = raw_input('');
'''