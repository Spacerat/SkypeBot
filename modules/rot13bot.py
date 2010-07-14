
import interface
import codecs

def Handle(interface,command,args,messagetype):
    """!rot13 phrase - rot13 a phrase."""
    interface.Reply(codecs.encode(args, "rot13"),edit=True)
interface.ComHook("rot13",Handle,name="")
