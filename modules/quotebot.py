
import interface
import urllib2
import time

global t
t=0

def Handle(interface,command,args,messagetype):
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

    global t

    if t+10>time.time():
        interface.Reply("It takes about 10 seconds to read and consider a new topic.")
        return

    t = time.time()

    url = "http://www.iheartquotes.com/api/v1/random?source=oneliners"
    request = urllib2.Request(url,None,{})
    response = urllib2.urlopen(request)
    r = " ".join(response.readlines())
    interface.Message.Chat.Topic = r.rpartition('\n \n')[0].replace("\n",'')

interface.ComHook("quote",Handle,name='QOTD')
interface.ComHook("randomtopic",RandomTopic,"TopicBot")