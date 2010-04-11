
import interface
import feedparser
import json
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


def Handle(interface,command,arg,messagetype):
    args = arg.split()
    callback = interface.Reply
    name=''
    url=''
    etag=''
    modified = ''
    entry = 0
    contentonly = False
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

    cache=None
    for root, dirs, files in os.walk('data/feeds/'):
        if name in files:
            cache = feedparser.parse(open(root+name))
            etag = cache.etag
        else:
            f = feedparser.parse(url,etag)
            
            if f:
                if f.status == 304:
                    f=cache
                try:
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
                        json.dump(f,open('data/feeds/'+name,'w'),skipkeys=True)

                except IndexError:
                    callback('Feed has no entries')
                else:
                    callback('Failed to parse feed.')

            return False

interface.AddHook("feed",Handle,'FeedBot')
