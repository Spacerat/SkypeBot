
import interface
import random

def Handle(interface,command,args,messagetype):
    n=6
    try:
        n=int(args)
    except:
        n=6
    finally:
        interface.Reply(str(random.randint(1,n))+"!")



interface.AddHook("dice",Handle,name="DiceBot")
