# ----------------------------------------------------------------------------------------------------
#  Python / Skype4Py super Skype Bot

from msnp.session import SessionCallbacks
import msnlib
import msncb
import threading
import time
import select
import socket

#from modules.skype import MSNInterface
from modules.interface import RecieveMessage

msn = msnlib.msnd()
msn.cb = msncb.cb()

if __name__ == "__main__":
    Cmd = '';
    while not Cmd == 'exit':
        Cmd = raw_input('');

def init():
    global msn

    msn.email="spaceratbot@live.co.uk"
    msn.pwd="l0lwut?"
    msn.login()
    print msn.nick
    msn.sync()
    msn.change_status("online")
    
    threading.Thread(None,do_work)

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

def do_work():
	"""
	Here you do your stuff and send messages using m.sendmsg()
	This is the only place your code lives
	"""

	# wait a bit for everything to settle down (sync taking efect
	# basically)
	time.sleep(15)

	print '-' * 20 + 'SEND 1'
	print msn.sendmsg("spacerat3004@hotmail.com", "Message One")

	print '-' * 20 + 'SEND 2'
	print msn.sendmsg("spacerat3004@hotmail.com", "Message Two")

	# give time to send the messages
	time.sleep(30)

	# and then quit
	quit()
