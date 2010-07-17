
import interface

def Handle(interface,command,args,messagetype):
    """!cls n - Erases the last n messages."""
    for x in interface.Message.Chat.Messages[0:int(args)]:
        try:
            x.Body=""
        except:
            pass

interface.ComHook("cls",Handle,security=3,admin=True)
