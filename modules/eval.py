
import interface
import time
import math
import threading
import skype
import re
import random

def Handle(interface,command,args,messagetype):
    if command == 'run':
        if messagetype=='SENT':
                ExecThread(args,interface,type='run').start()
        else:
            interface.Reply("Permission denied!")

    if command=='eval':
            ExecThread(args,interface,type='eval').start()

class ExecThread(threading.Thread):
    def __init__(self,code,interface,type='eval'):
        threading.Thread.__init__(self)
        self.i = interface
        self.code = code
        self.type = type

    def run(self):
        if self.type=='run':
            i = self.i
            r = self.r
            exec self.code
        elif self.type=='eval':
            try:
                locals = {
                    #Math
                    'pow': pow,
                    'ceil': math.ceil,
                    'floor': math.floor,
                    'round': round,
                    'log': math.log,
                    'log10': math.log10,
                    'e': math.e,
                    'pi': math.pi,
                    'sqrt': math.sqrt,
                    'complex': complex,
                    'abs': abs,

                    #Lists
                    'range': range,
                    'map': map,
                    'filter': filter,
                    'reduce': reduce,
                    'zip': zip,
                    'enumerate': enumerate,
                    'any': any,
                    'all': all,
                    
                    #String
                    'str': str,
                    'chr': chr,
                    'bin': bin,

                    #Skype
                    'i': self.i,
                    '__builtins__': None,
                }
                locals['l']=locals
                r=eval(self.code,{'__builtins__':None,},locals)
                del locals['l']
                s=str(r)
                if len(s)>400: s = s[0:400]+" ..."
                self.i.Reply(s)
            except Exception as e:
                self.i.Reply("Error: "+str(e))

    def r(self,text):
        if text=='': return
        self.i.Reply(text)

interface.AddHook('run',Handle)
interface.AddHook('eval',Handle,name="EvalBot")
