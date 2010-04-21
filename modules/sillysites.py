
import interface

def Handle(interface,command,args,messagetype):
    rep=''
    if command=='rimshot':

        rep=r'http://instantrimshot.com/'
    elif command=='trombone':
        rep=r'http://www.sadtrombone.com/'
    elif command=='buuurn':
        rep=r'http://buuurn.com/'

    try:
        interface.Message.Body = rep
    except:
        interface.Reply(rep)

interface.AddHook("rimshot",Handle)
interface.AddHook("trombone",Handle)
interface.AddHook("buuurn",Handle)
