
import interface
import threading
from datetime import datetime, timedelta, time, date
import getopt
import json
import pickle

interfaces=[]

def AddInterface(i):
    interfaces.append(i)

def AdvSplit(s):
    split = s.split()
    result = []
    inquote=False
    i=-1
    for x in split:
        if inquote == False:
            result.append(x)
            i+=1
        else:
            result[i] = result[i] + " " + x
        if x.count('"')%2 != 0:
            if inquote == False:
                inquote = True
            else:
                inquote = False

    return result

class EventException(BaseException):
    def __init__(self,message,dt=None):
        self.message = message
        self.dt = dt
    def __str__(self):
        return self.message.format(self.dt)

def DoEvent(a):
    global interfaces
    for i in interfaces:
        i.Reply(a)

def LoadEvents():
    url = "data/schedule.txt"

    f=open(url)
    d = json.load(f)

    for t in d:
        dt = datetime.strptime(t,"%Y/%m/%d %H:%M")
        s = (dt - datetime.now()).seconds
        for x in d[t]:
            threading.Timer(s,DoEvent, [x]).start()

def AddEvent(dt,message):
    url = "data/schedule.txt"
    str = dt.strftime("%Y/%m/%d %H:%M")
    try:
        f=open(url)
        d = json.load(f)
    except IOError:
        f=open(url,"w")
        f.write("{}")
        f.close()
        f=open(url)
        d=json.load(f)
    except ValueError:
        f.close()
        f = open(url,"w")
        f.write("{}")
        f.close()
        f=open(url)
        d=json.load(f)
    f.close()
    if not str in d:
        d[str] = []

    d[str].append(message)
    
    f= open(url,'w')
    json.dump(d,f)
    f.close()

def ScheduleUsage(interface):
    interface.Reply("Use !schedule [-r] [-d dd/mm/yy] MM:HH Message")

def ScheduleHandle(interface,command,t,messagetype):
    l = AdvSplit(t)

    try:
        optlist, args = getopt.getopt(l,'rd:')
    except getopt.GetoptError, err:
        interface.Reply(str(err))
        ScheduleUsage(interface)
        return

    if len(args)!=2:
        interface.Reply("Wrong number of arguments.")
        ScheduleUsage(interface)
        return

    recurring = False
    datestr = ''

    for o, a in optlist:
        if o=='-r': recurring = True
        if o=='-d': datestr = a
    timestr=args[0]
    message = args[1].replace('"',"")

    if datestr!="":
        sdate = datetime.strptime(datestr,"%d/%m/%y")
    else:
        sdate = datetime.today()
    stime = datetime.strptime(timestr,"%H:%M")
    
    sdatetime = datetime(sdate.year,sdate.month,sdate.day,stime.hour,stime.minute)
    try:
        AddEvent(sdatetime,message)
    except EventException, err:
        print str(err)


    s = (sdatetime - datetime.now()).seconds
    threading.Timer(s,DoEvent, [message]).start()


def InitSchedulerHandle(interface,command,t,messagetype):
    AddInterface(interface)

ScheduleHandle(interface.DebugInterface(),"schedule","01:11 bleep",'SENT')

LoadEvents()



interface.ComHook("schedule",ScheduleHandle,name="AlarmBot")
interface.ComHook("initschedule",InitSchedulerHandle,name="AlarmBot")
