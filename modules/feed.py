
import interface
import feedparser
import json
import pickle
import os

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


def Handle(interface,command,arg,messagetype,entry=0,contentonly=False):
    """!feed [name] [url] - Fetches the latest item from a feed.
    If only url is supplied, the latest item from that feed is fetched.
    If only name is supplied, the latest item from the feed saved under name is fetched.
    If name and url are supplied, url is added to the saved feed list under name, if the fetch is successful.
    """
    args = arg.split()
    callback = interface.Reply
    name=''
    url=''
    etag=''
    modified = ''
    
    if len(args)==0:
        interface.Reply('use !feed [name] url')
    elif len(args)==1:
        if args[0] in Feeds['alias']:
            name = args[0]
            url = Feeds['alias'][name]
        else:
            url = args[0]
    elif len(args)==2:
        name = args[0]
        url = args[1]
        Feeds['alias'][name]=url
        ExportFeedsJSON()

    cache=None
    for root, dirs, files in os.walk('data/feeds/'):
        if name in files:
            cache = pickle.load(open(root+name))
            #print 'cache loaded'
            etag = cache.get('etag','')
            modified = cache.get('modified','')

            #print 'etag',etag
            #print 'url',url
            #print 'modified',modified

    f = feedparser.parse(url,etag=etag,modified=modified)
    if f:
        #print 'status: ',f.status
        s= f.get('status',200)
        if s == 304:
            #print '304: using cache'
            f=cache
        elif s == 301:
            if name:
                Feeds['alias'][name]=f.get('href',url)
    if f['feed']:
        e = f['entries'][entry]
        upstring =''
        if 'updated' in e: upstring =  " ("+e.updated+")"
        if not contentonly:
            if len(f)<25:
                callback(f['feed']['title']+" - "+e.title+upstring)
            else:
                callback(f['feed']['title'])
                callback(e.title+upstring)
        tag=''
        s=''

        if 'summary' in e:
            tag = 'summary'
        elif 'subtitle' in e:
            tag = 'subtitle'
        elif 'content' in e:
            tag = 'content'

        s=e[tag]
        if tag: callback(FormatHTML(s)[0:min(len(s),500)])

        if not contentonly and 'link' in e: callback(e.link)

        if cache == None:
            pickle.dump(f,open('data/feeds/'+name,'w'))

def FMLHandle(interface,command,arg,messagetype):
    """!fml [n] - Retrieves the latest or nth FML."""
    try:
        e=int(arg)-1
        if e>35:
            interface.Reply('FML Number must be between 1 and 35')
            return
        Handle(interface,command,'fml',messagetype,entry=e,contentonly=True)
    except:
        Handle(interface,command,'fml',messagetype,contentonly=True)

interface.ComHook("feed",Handle,name='FeedBot')
interface.ComHook("fml",FMLHandle,name='FMLBot')

LoadFeedsJSON(os.path.abspath("data/feeds.txt"))