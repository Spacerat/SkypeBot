
from security import *
import interface

def GetSecurityCom(i,command,args,messagetype):
    handle=''
    nick = args
    if len(args)>0:
        try:
            handle=i.Users.get(args,args)
            nick = args
        except:
            handle=args
    else:
        handle=i.UserAddress
        nick = i.UserName

    i.Reply("%s has an access level of %u"%(nick,GetSecurityForHandle(i,handle)))
    if GetAdminForHandle(i,handle):
        i.Reply("%s can perform admin commands in this conversation."%nick)
    else:
        i.Reply("%s cannot perform admin commands in this conversation."%nick)

def SetSecurityLevelCom(i,command,args,messagetype):
    args=args.rpartition(" ")
    n=args[0]
    l=int(args[2].strip())

    try:
        handle=i.Users.get(n,n)
    except:
        handle = n
    curlevel = GetSecurityForHandle(i,handle)
    rhandle=i.UserAddress
    rlevel = GetSecurityForHandle(i,rhandle)
    if rlevel>curlevel and l<rlevel:
        SetSecurityForHandle(i,handle,l)
        i.Reply("Set %s to level %u"%(n,l))
    else:
        i.Reply("You can only set the level of someone lower than you to a level lower than your own.")
def SetConvoAdmin(i,command,args,messagetype):
    args=args.rpartition(" ")
    n=args[0]
    l=(int(args[2].strip())==True)
    handle=i.Users.get(n,n)
    curlevel = GetSecurityForHandle(i,handle)
    rhandle=i.UserAddress
    rlevel = GetSecurityForHandle(i,rhandle)
    radmin = GetAdminForHandle(i,rhandle)
    if not radmin and l==True:
        i.Reply("Only admins can make other people admins.")
        return
    if rlevel<curlevel:
        i.Reply("You cannot change the admin status of those with a higher access level than you.")
        return
    SetAdminForHandle(i,handle,l)
    if l==True:
        i.Reply("%s can now use admin commands in this conversation."%n)
    else:
        i.Reply("%s can no longer use admin commands in this conversation."%n)

interface.ComHook("getlevel",GetSecurityCom,name="AccessBot")
interface.ComHook("setlevel",SetSecurityLevelCom,name="AccessBot")
interface.ComHook("setadmin",SetConvoAdmin,name="AccessBot")