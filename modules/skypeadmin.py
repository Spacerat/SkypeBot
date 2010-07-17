
#Time for some serious power-abuse facilitation.

import interface
import threading

def GetMemberObject(interface,handle):
    for x in interface.Message.Chat.MemberObjects:
        if x.Handle==handle: return x

def CheckAccess(interface,name):
    if not interface.Type=="Skype": return False
    x = GetMemberObject(interface,name)
    if (x.Role=='CREATOR' or x.Role=='MASTER'):
            return True
    return False

def SetRole(interface,name,member,role):
    if member.CanSetRoleTo(role):
        try:
            member.Role=role

        except:
            pass
        print name,role
        interface.Reply("/me sets %s to %s"%(name,role))


def Mute(i,command,args,messagetype):
    """!mute nick/handle minutes - mutes a user for a number of minutes"""
    args = args.rpartition(" ")
    """
    if args[2]=="":
        i.Name="Help"
        interface.HelpHandle(i,'help','mute',messagetype)
        return
    """
    handle = i.Users.get(args[0],args[0])

    member = GetMemberObject(i,handle)
    SetRole(i,args[0],member,'LISTENER')

    threading.Timer(float(args[2])*60,SetRole,[i,args[0],member,'USER']).start()



interface.ComHook("mute",Mute,admin=True)