
import interface
import random
import time

random.seed(time.time())

def Handle(interface,command,args,messagetype):
    """!8ball question - Invoke the magic 8ball..."""
    ballfile = open("data/8ball.txt")
    lines = ballfile.readlines()
    if not args.endswith("?"):
        args=args+"?"
    interface.Reply(args+" "+lines[random.randint(0,len(lines)-1)])


interface.ComHook("8ball",Handle,name="8Ball")
