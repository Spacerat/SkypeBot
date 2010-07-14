
import interface
import json

def LoadData(url):
    global data
    global durl
    f=open(url)
    if f:
        data = json.load(f)
        f.close()
        durl = url

def ExportData():
    global datafile
    global durl

    f = open(durl,'w')
    if f: json.dump(data,f)


def Handle(interface,command,args,messagetype):
    global data
    

    if len(args)>0:
        if args.lower() == "conversation":
            interface.Reply("The conversation cannot win.")
            return
        if not args.capitalize() in data:
            if (interface.UserAddress=='spacerat3004' or interface.UserAddress=='loquaciousgirl'):
                data[args.capitalize()]=1
        else:
            if command=="convokill":
                if (interface.UserAddress=='spacerat3004' or interface.UserAddress=='loquaciousgirl'):
                    data[args.capitalize()]=data[args.capitalize()]+1
            elif command=="convounkill":
                if (interface.UserAddress=='spacerat3004' or interface.UserAddress=='loquaciousgirl'):
                    data[args.capitalize()]=data[args.capitalize()]-1
                if data[args.capitalize()]==0:
                    del data[args.capitalize()]
        interface.Reply(args+": "+str(data[args.capitalize()])+"  Conversation: 0")
        ExportData()

    else:
        r=""
        for x in iter(data):
            r=r+"%s: %u  "%(x,data[x])
        r+="  Conversation: 0"
        interface.Reply(r)


interface.ComHook("convokill",Handle,"KillBot")
interface.ComHook("convounkill",Handle,"KillBot")