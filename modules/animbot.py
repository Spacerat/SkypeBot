
import interface
import time
import threading

def Handle(interface,command,args,messagetype):

    if interface.IsEditable:
        AnimThread(interface,args).start()


class AnimThread(threading.Thread):
    """!anim [text] - Create a stupid little test animation with optional stupid text."""
    def __init__(self,interface,text=''):
        threading.Thread.__init__(self)
        self.it=interface
        self.text=text
    def run(self):
        Go = True
        ltime = time.time()
        otime = time.time()+20.4
        x=0
        dir=1
        while Go:
            if time.time()>ltime:
                ltime=ltime+0.3
                if self.it.IsEditable:
                    if self.text=='':
                        ar=""
                        if dir==1:
                            ar=">"
                            x+=1
                            if x==10: dir=0
                        else:
                            ar="<"
                            x-=1
                            if x==0: dir=1

                        self.it.Reply("-"*x+ar+"-"*(10-x),edit=True)
                    else:
                        x = 1-x
                        if x==1:
                            self.it.Reply(self.text,edit=True)
                        else:
                            self.it.Reply("-"*len(self.text),edit=True)
                else:
                    Go=False
                if time.time()>otime:
                    Go = False

interface.ComHook("anim",Handle)
