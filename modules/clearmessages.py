
import interface

def Handle(interface,command,args,messagetype):
    if messagetype=='SENT':
        for x in interface.Message.Chat.Messages[0:int(args)]:
            try:
                x.Body=""
            except:
                pass

interface.ComHook("cls",Handle,hidden=True)
