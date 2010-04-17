
import interface

def Handle(interface,command,args,messagetype):
    interface.Reply(args)

interface.AddHook("echo",Handle,name='EchoBot')
