
import interface

def Handle(interface,command,args,messagetype):
    """!rimshot = http://instantrimshot.com/
    !trombone = http://www.sadtrombone.com/
    !buuurn = http://buuurn.com/
    !nooo = http://www.nooooooooooooooo.com/"""

    if command=='rimshot':
        interface.Reply(r'http://instantrimshot.com/',edit=True)
    elif command=='trombone':
        interface.Reply(r'http://www.sadtrombone.com/',edit=True)
    elif command=='buuurn':
        interface.Reply(r'http://buuurn.com/',edit=True)
    elif command=='nooo':
        interface.Reply(r'http://www.nooooooooooooooo.com/',edit=True)

interface.ComHook("rimshot",Handle)
interface.ComHook("trombone",Handle)
interface.ComHook("buuurn",Handle)
interface.ComHook("nooo",Handle)
