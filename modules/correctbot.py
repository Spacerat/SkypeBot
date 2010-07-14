
import interface
from stringsafety import *
import enchant
from enchant.tokenize import get_tokenizer, EmailFilter, URLFilter
from random import randint
import json

d = enchant.Dict("en_UK")
tkn = get_tokenizer("en_UK",filters=[EmailFilter, URLFilter])
enabled=True

def LoadReplaceDict(url=""):
    global replaceurl
    global repdict

    if url!="": replaceurl = url
    f = open(replaceurl)
    if f:
        repdict = json.load(f)
        f.close()

def SaveReplaceDict(url=""):
    global replaceurl

    if url!="": replaceurl = url
    f = open(replaceurl,"w")
    json.dump(repdict,f)
    f.close()

def Handle(interface,text):
        
    if "ReplaceBot:" in text: return
    '''
    if enabled:
        if not interface.Message.IsEditable: return
        
        orig = text
        for w in tkn(text):

            if d.check(w[0]) == False:
                r = d.suggest(w[0])
                if r:
                   text = text.replace(w[0],r[0])
        if orig!=text:
            interface.Message.Body = text

    '''
    if enabled:

        try:
            if not interface.IsEditable:
                return
        except:
            return

        global repdict

        repmessage = text

        for word in repdict:

            while word.lower() in repmessage.lower():
                pos = repmessage.lower().find(word.lower())
                cword = repmessage[pos:pos+len(word)]
                replace=""
                if cword.isupper():
                    replace = repdict[word].upper()
                elif cword.islower():
                    replace = repdict[word].lower()
                elif cword.istitle():
                    replace = repdict[word].capitalize()
                else:
                    replace = repdict[word]

                repmessage = repmessage.replace(cword,replace,1)

            if text!=repmessage:
                interface.Reply(repmessage,edit=True)
		
def ToggleSpeller(interface,command,args,messagetype):
    """!autoreplace - Turns on/off the autoreplace bot."""
    global enabled

    if not enabled:
        enabled=True
        LoadReplaceDict()
        interface.Reply("Replacebot enabled!")
    else:
        enabled=False
        interface.Reply("Replacebot disabled.")

def AddReplace(interface,command,args,messagetype):
    """!replace word->replacement - Adds a word to replacebot's replacement dictionary.
    The word before -> gets replaced by the word after ->."""
    global repdict

    args=args.split("->")

    if len(args)!=2:
        interface.Reply("Use %sreplace old-phrase->new-phrase" %interface.GetPrefix())
        return
    args[0]=args[0].strip().lower()
    args[1]=args[1].strip().lower()

    if "joe" in args[0].lower():
        args[1]="god"

    if args[0] in args[1]:
        interface.Reply("You cannot replace a word with itself.")
        return

    for v in repdict:
        if args[0] in repdict[v]:

            interface.Reply("You cannot replace %s with %s because %s already replaces to %s" % (args[0],args[1],v,args[0]))
            return
    
    repdict[args[0].lower()]=args[1].lower()
    SaveReplaceDict()

    interface.Reply("Replacing %s with %s" % (args[0].lower(),args[1].lower()))

def RemoveReplace(interface,command,args,messagetype):
    """!unreplace word - Removes a word from replacebot's replacement dictionary.
    You must type the word you want to unreplace, not its replacement."""
    global repdict

    args=args.lower()

    del repdict[args.lower()]

    f = open(replaceurl,"w")
    json.dump(repdict,f)
    f.close()
    SaveReplaceDict()

    interface.Reply("%s is no longer replaced" % args.capitalize())

def GetReplacements(interface,command,args,messagetype):
    """!getreplacements - shows all words currently being replaced."""
    global repdict
    r='\n'
    for x in repdict:
        r=r+"%s -> %s\n"%(x,repdict[x])
    interface.ReplyToSender(r)

def ClearReplacements(interface,command,args,messagetype):
    """!clearreplacements - wipes the replacebot dictionary"""
    global repdict
    repdict = {}
    SaveReplaceDict()

interface.MessageHook(Handle)
interface.ComHook("autoreplace",ToggleSpeller,name="ReplaceBot")
interface.ComHook("replace",AddReplace,"ReplaceBot")
interface.ComHook("unreplace",RemoveReplace,"ReplaceBot")
interface.ComHook("getreplacements",GetReplacements,"ReplaceBot")
interface.ComHook("clearreplacements",ClearReplacements,"ReplaceBot",status='SENT',hidden=True)
