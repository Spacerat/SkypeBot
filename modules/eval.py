
import interface
import time
import math
import threading
import skype
import re
import random
import security

def RunHandle(interface,command,args,messagetype):
    RunThread(interface,args).start()

def EvalHandle(interface,command,args,messagetype):
    """!ev message {expression} message - Outputs/edits a message, evaluating python expressions inside curly brackets.
    For example, !ev There are {60*2*60} seconds in two hours.
    """

    lock = threading.Lock()
    editing = True

    try:
        interface.Message.Body = args
        message = interface.Message
    except:
        editing = False
        message = EvalMessage(args)

    while True:
        l = args.find("{")
        if l>=0:
            r = args.find("}")
            sect=args[l:(r+1)]
            code = args[(l+1):r]
            
            t = ExecThread(message,sect,code,mode='edit',lock=lock)
            t.start()
            if not editing: t.join(10)
            args = args[(r+1):len(args)]
        else:
            break
            
    if editing == False:
        interface.Reply(message.Body)


class EvalMessage:
    def __init__(self,body):
        self.Body = body

class RunThread(threading.Thread):
    def __init__(self,interface,code):
        threading.Thread.__init__(self)
        self.i = interface
        self.code = code
    def run(self):
        i = self.i
        r = self.r
        exec self.code

    def r(self,text):
        if text=='': return
        self.i.Reply(text)

class ExecThread(threading.Thread):
    def __init__(self,message,replace,code,mode='reply',lock=None):
        threading.Thread.__init__(self)
        self.message = message
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
                #'i': self.i,

                '__builtins__': None,
            }
            locals['l']=locals
            r=eval(self.code,{'__builtins__':None,},locals)
            del locals['l']
            s=str(r)
            if len(s)>400: s = s[0:400]+" ..."

            if (self.lock):
                self.lock.acquire()
            self.message.Body = self.message.Body.replace(self.replace,s)
            if (self.lock):
                self.lock.release()

        except None as e:
            #raise e
            self.i.Reply("Error: "+str(e))

    def r(self,text):
        if text=='': return
        self.i.Reply(text)

interface.ComHook('run',RunHandle,security=4)
interface.ComHook('ev',EvalHandle,name="EvalBot",security=2)
