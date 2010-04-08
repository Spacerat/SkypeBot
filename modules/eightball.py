
import interface
import random
import time

random.seed(time.time())

def Handle(interface,command,args,messagetype):
    ballfile = open("data/8ball.txt")
    lines = ballfile.readlines()
    if not args.endswith("?"):
        args=args+"?"
    interface.Reply(args+" "+lines[random.randint(0,len(lines)-1)])


interface.AddHook("8ball",Handle,"8Ball")
