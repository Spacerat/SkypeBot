
import interface
import time

global t
t=0

def Handle(interface,command,args,messagetype):
    interface.Reply(args)

def HelloHandle(interface,command,args,messagetype):

    global t

    if t+20>time.time():
        return
    t = time.time()

    r = ''
    for x in interface.Users:
        r+=x+"! "
    interface.Reply(r)

interface.ComHook("hello",HelloHandle)
interface.ComHook("echo",Handle,name='EchoBot')
