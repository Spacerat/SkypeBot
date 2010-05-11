
import interface
from stringsafety import *
import enchant
from enchant.tokenize import get_tokenizer, EmailFilter, URLFilter
from random import randint

d = enchant.Dict("en_UK")
tkn = get_tokenizer("en_UK",filters=[EmailFilter, URLFilter])
enabled=False

def Handle(interface,text):

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


    else:
        if "your're" in text.lower():
            text=text.replace("your're","<your're does not exist you idiot>")
            if interface.Message.IsEditable:
                interface.Message.Body = text
        if "whos" in text.lower() and not "whose" in text.lower():
            text=text.replace("whos","<whos does not exist you extreme fish>")
            if interface.Message.IsEditable:
                interface.Message.Body = text
        if "sik3d" in text.replace(" ","").lower() or "sick3d" in text.replace(" ","").lower():
            text=text.replace("3d","<sik3d is lame and you should stop using it.>")
            if interface.Message.IsEditable:
                interface.Message.Body = text
        #if text.isupper():
        #    interface.Reply("CAPS CAPS CAPS!!! xD")

def ToggleSpeller(interface,command,args,messagetype):
    global enabled
    if not enabled:
        enabled=True
        interface.Reply("Retarded auto-spellbot enabled!")
    else:
        enabled=False
        interface.Reply("Retarded auto-spellbot disabled.")

interface.MessageHook(Handle)
interface.ComHook("autospeller",ToggleSpeller,name="SpellBot")
