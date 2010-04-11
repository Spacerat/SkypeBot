
import interface

def Handle(interface,command,args,messagetype):
    interface.Reply(r'http://instantrimshot.com/')

interface.AddHook("rimshot",Handle,'')
