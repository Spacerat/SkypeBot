
import interface
import urllib2
import time
import math

global t
t=0

def Handle(interface,command,args,messagetype):
    """!fortune [categories] - Retrieves a random quote from iheartquotes.com.
    The quote is retrieved from a random category in a list of categores separated by +, if the list is supplied."""

    source=''
    if args:
        args = args.replace(" ","_")
        source="source="+args

    url = "http://www.iheartquotes.com/api/v1/random?max_characters=500&"+source
    request = urllib2.Request(url,None,{})
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError as e:
        if e.code == 500:
            interface.Reply("Category '"+args+"' does not exist!")
        else:
            interface.Reply(str(e.code)+" error.")
        return
  #  for x in response.readlines():
  #      interface.Reply(x)
    r = " ".join(response.readlines())
    # @type r str
    r = r.rpartition('\n \n')
    interface.Reply(r[0].replace("\n",''))

def RandomTopic(interface,command,args,messagetype):
    """!randomtopic - Sets a random conversation topic. Can only be used once every 20 seconds."""
    global t

    if t+20>time.time():
        interface.Reply("Wait "+str(int(t+20-time.time()))+" seconds.")
        return
    t = time.time()

    url = "http://www.iheartquotes.com/api/v1/random?source=oneliners+why+sex+misc+technology"
    request = urllib2.Request(url,None,{})
    response = urllib2.urlopen(request)
    r = " ".join(response.readlines())

    text = unicode(r.rpartition('\n \n')[0].replace("\n",''),errors='ignore')

    interface.SetTopic(text)

interface.ComHook("fortune",Handle,name='QOTD')
interface.ComHook("randomtopic",RandomTopic,"TopicBot")
