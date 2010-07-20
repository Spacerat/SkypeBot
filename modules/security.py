
import json

def LoadData(url):
    global data
    global durl
    durl = url
    f=None
    try:
        f=open(url)
    except:
        data = {}
        ExportData()
        return

    if f:
        data = json.load(f)
        f.close()
        durl = url

def ExportData():
    global data
    global durl

    f = open(durl,'w')
    if f:
        json.dump(data,f)
        f.close()


def GetSecurityForHandle(i,handle):
    global data
    if handle==i.BotHandle: return 5

    try:
        r = data[handle].get('sec',1)
        return r
    except:
        return 1
def GetAdminForHandle(i,handle):
    global data
    if handle==i.BotHandle: return 1
    try:
        r = data[handle].get(i.ChatName,0)
        return r
    except:
        return 0
def SetSecurityForHandle(i,handle,security):
    global data
    if handle not in data: data[handle]={}
    data[handle]['sec']=security
    ExportData()
def SetAdminForHandle(i,handle,admin):
    global data
    if handle not in data: data[handle]={}
    data[handle][i.ChatName]=admin
    ExportData()

LoadData("data/access.txt")