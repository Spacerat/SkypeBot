
import interface
import urllib2
import re
from xml.dom import minidom
from stringsafety import *
from random import randint

def Handle(interface,command,args,messagetype):
    if args=="": return
    url = "http://www.zachblume.com/apis/rhyme.php?format=xml&word="+escapeurl(args)
    request = urllib2.Request(url,None,{'Referer':'http://spacerat.meteornet.net'})
    response = urllib2.urlopen(request)
    words = []
    
    for x in response.readlines():
        words.append(FormatHTML(x))

    if len(words)==2:
        interface.Reply('No rhymes for you. Sorry :(')
        return
    
    say = ''
    for i in range(0,4):
        app=''
        while True:
            app = words[randint(0,len(words)-1)]
            app=app[0:len(app)-1]
            if not app in say:
                break
        say+=app+"  "

    if say: interface.Reply(say)


interface.AddHook("rhyme",Handle,name="RhymeBot")