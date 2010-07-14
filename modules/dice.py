
import interface
import random

def Handle(interface,command,args,messagetype):
    """!dice [max] - Says a number between (inclusive) 1 and 6, or 1 and max"""
    n=6
    try:
        n=int(args)
    except:
        n=6
    finally:
        interface.Reply(str(random.randint(1,n))+"!")



interface.ComHook("dice",Handle,name="DiceBot")
