
import interface
import feedparser
import json
from stringsafety import *

datafile = ''
Feeds = {}

def LoadFeedsJSON(url):
    global Feeds
    global datafile
    f=open(url)
    if f:
        Feeds = json.load(f)
        datafile = url
        f.close()

def ExportFeedsJSON(url=''):
    global datafile
    if url=='': url = datafile
    f = open(url,'w')
    if f: json.dump(Feeds,f)

def ReplyFeed(callback,url):
    f = feedparser.parse(url)
    if f:
        try:
            e = f['entries'][0]
            upstring =''
            if 'updated' in e: upstring =  " ("+e.updated+")"
            if len(f)<25:
                callback(f['feed']['title']+" - "+e.title+upstring)
            else:
                callback(f['feed']['title'])
                callback(e.title+upstring)
            callback(e.summary)
            if 'link' in e: callback(e.link)
            return True
        except IndexError:
            callback('Feed has no entries')
        else:
            callback('Failed to parse feed.')

    return False

def Handle(interface,command,args,messagetype):
    # @type args str
    #args = args.replace(' ','+')
    #url = r'http://newsrss.bbc.co.uk/rss/newsonline_uk_edition/front_page/rss.xml'
    success = True
    argl=args.split()
    name=''

    if len(argl)>0:
        name = argl[0].lower()
        if name in Feeds:
            url=Feeds[name]
            success = ReplyFeed(interface.Reply,url)
        elif len(argl)==1:
            url=argl[0]
            success = ReplyFeed(interface.Reply,url)
        elif len(argl)==2:
            url=argl[1]
            f = feedparser.parse(url)
            if f:
                success = ReplyFeed(interface.Reply,url)
                if success:
                    Feeds[argl[0].lower()]=url
                    ExportFeedsJSON()
            else:
                success = False
    else:
        success = False

    if success == False:
        interface.Reply('Unable to get feed data.')

def FeedsHandle(interface,command,args,messagetype):
    for x in Feeds.keys():
        interface.Reply('{0}: {1}'.format(x,Feeds[x]))

interface.AddHook("feed",Handle,"FeedBot")
interface.AddHook("feeds",FeedsHandle,"FeedBot")