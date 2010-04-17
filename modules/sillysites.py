
import interface

def Handle(interface,command,args,messagetype):
    if command=='rimshot':
        interface.Reply(r'http://instantrimshot.com/')
    elif command=='trombone':
        interface.Reply(r'http://www.sadtrombone.com/')


interface.AddHook("rimshot",Handle)
interface.AddHook("trombone",Handle)
