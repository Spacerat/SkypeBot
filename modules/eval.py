
import interface
import time
import math
import threading
import skype
import re
import random

def Handle(interface,command,args,messagetype):

    if messagetype=='SENT':
        if command == 'run':
                ExecThread(args,interface,type='run').start()
        elif command=='eval':
            s = re.compile("\(\)")
            args = s.sub('',args)
            ExecThread(args,interface,type='eval').start()
    else:
        interface.Reply("Permission denied!")

class ExecThread(threading.Thread):
    def __init__(self,code,interface,type='eval'):
        threading.Thread.__init__(self)
        self.i = interface
        self.code = code
        self.type = type

    def run(self):
        if self.type=='run':
            i=self.i
            r=i.Reply
            exec self.code
        elif self.type=='eval':
            try:
                self.i.Reply(eval(self.code,None,locals()))
            except Exception as e:
                self.i.Reply("Error: "+str(e))




interface.AddHook('run',Handle)
interface.AddHook('eval',Handle,name="EvalBot")
