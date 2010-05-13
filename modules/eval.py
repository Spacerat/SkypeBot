
import interface
import time
import math
import threading
import skype
import re
import random

def RunHandle(interface,command,args,messagetype):
    if messagetype=='SENT':
            RunThread(interface,args).start()
    else:
        interface.Reply("Permission denied!")


def EvalHandle(interface,command,args,messagetype):

    lock = threading.Lock()
    editing = True
    try:
        interface.Message.Body = args
    except:
        editing = False

    if editing:
        while True:
            l = args.find("{")
            if l>=0:
                r = args.find("}")
                sect=args[l:(r+1)]
                code = args[(l+1):r]
                ExecThread(interface,sect,code,mode='edit',lock=lock).start()
                args = args[(r+1):len(args)]
            else:
                break
    else:
        ExecThread(interface,args,args,mode='reply')

class RunThread(threading.Thread):
    def __init__(self,interface,code):
        threading.Thread.__init__(self)
        self.i = interface
        self.code = code
    def run(self):
        i = self.i
        r = self.r
        exec self.code


class ExecThread(threading.Thread):
    def __init__(self,interface,replace,code,mode='reply',lock=None):
        threading.Thread.__init__(self)
        self.i = interface
        self.code = code
        self.replace = replace
        self.lock = lock
        self.mode = mode

    def run(self):

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

                #Interface
                'i': self.i,

                '__builtins__': None,
            }
            locals['l']=locals
            r=eval(self.code,{'__builtins__':None,},locals)
            del locals['l']
            s=str(r)
            if len(s)>400: s = s[0:400]+" ..."
            if mode=='edit':
                if (self.lock):
                    self.lock.acquire()
                self.i.Message.Body = self.i.Message.Body.replace(self.replace,s)
                if (self.lock):
                    self.lock.release()
            elif mode=='reply':
                self.i.Reply(s)

        except None as e:
            #raise e
            self.i.Reply("Error: "+str(e))

    def r(self,text):
        if text=='': return
        self.i.Reply(text)

interface.ComHook('run',RunHandle,hidden=True)
interface.ComHook('ev',EvalHandle,name="EvalBot")
