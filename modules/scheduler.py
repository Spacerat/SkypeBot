
import interface
import threading
from datetime import datetime, timedelta, time, date
import getopt
import json
import random

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

def DoEvent(timestr,id,message,recur):
    global interfaces
    url = "data/schedule.txt"
    for i in interfaces:
        i.Reply(message)

    f=open(url,'r')
    d=json.load(f)
    f.close()

    del d[timestr][str(id)]
    if len(d[timestr])==0:
        del d[timestr]


    f = open(url,'w')
    json.dump(d,f)
    f.close()

    

    t = datetime.strptime(timestr,"%Y/%m/%d %H:%M")

    if recur=='day':
        t = t + timedelta(days=1)
    if recur=='week':
        t = t + timedelta(weeks=1)
    if recur=='hour':
        t = t + timedelta(hours=1)
    if recur=='minute':
        t = t + timedelta(minutes=1)
    if recur=='year':
        t = t + timedelta(days=365)

    if recur!="":
        AddEvent(t,message,recur=recur)
    
def LoadEvents():
    url = "data/schedule.txt"
    try:
        f=open(url)
        d = json.load(f)
    except:
        return
    
    for t in d:
        dt = datetime.strptime(t,"%Y/%m/%d %H:%M")
        delta = (dt-datetime.now())
        secs = delta.seconds + delta.days*86400
        for e in d[t]:
            message=d[t][e]['message']
            recurrence=d[t][e]['recurrence']
            threading.Timer(secs,DoEvent, [t,e,message,recurrence]).start()
            

def AddEvent(dt,message,recur=''):
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
        d[str] = {}

    e = random.randint(0,65536)
    d[str][repr(e)]={"message":message,"recurrence":recur}
    
    f= open(url,'w')
    json.dump(d,f)
    f.close()

    delta = (dt - datetime.now())
    secs = delta.seconds + delta.days*86400

    threading.Timer(secs,DoEvent, [str,e,message,recur]).start()

def ScheduleUsage(interface):
    interface.Reply("Use !schedule [-r year/week/day/hour] [-d dd/mm/yy] MM:HH Message")

def ScheduleHandle(interface,command,t,messagetype):
    l = AdvSplit(t)

    try:
        optlist, args = getopt.getopt(l,'r:d:')
    except getopt.GetoptError, err:
        interface.Reply(str(err))
        ScheduleUsage(interface)
        return

    if len(args)!=2:
        interface.Reply("Wrong number of arguments.")
        ScheduleUsage(interface)
        return

    recur = ''
    datestr = ''

    for o, a in optlist:
        if o=='-r': recur = a
        if o=='-d': datestr = a
    timestr=args[0]
    message = args[1].replace('"',"")

    if datestr!="":
        try:
            sdate = datetime.strptime(datestr,"%d/%m/%y")
        except ValueError, err:
            interface.Reply(str(err))
    else:
        sdate = datetime.today()
    stime = datetime.strptime(timestr,"%H:%M")
    
    sdatetime = datetime(sdate.year,sdate.month,sdate.day,stime.hour,stime.minute)
    try:
        AddEvent(sdatetime,message,recur=recur)
    except EventException, err:
        print str(err)


def InitSchedulerHandle(interface,command,t,messagetype):
    AddInterface(interface)
    
LoadEvents()


interface.ComHook("schedule",ScheduleHandle,name="AlarmBot")
interface.ComHook("initschedule",InitSchedulerHandle,name="AlarmBot")
