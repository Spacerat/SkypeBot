
import interface
from BeautifulSoup import BeautifulSoup
from stringsafety import *
import urllib2
import re

#A few bits and bobs from KittyBot once again. I, however, shall be making my life easier with BeautifulSoup.
def load_url(url):
    handle = urllib2.urlopen(urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-US; rv:1.9.0.10) Gecko/2009042316 Firefox/3.0.10', 'Referrer': 'http://spacerat.meteornet.net'}))
    data = handle.read().decode('utf-8')
    handle.close()
    return data

def GetPage(args=''):
    args = args.replace(" ","%20")

    if len(args) == 0:
        page = 'Special:Random'
    else:
        page = args.replace(' ','_')
    url = 'http://en.wikipedia.org/wiki/%s' % escapeurl(page)
    try:
        response = load_url(url)
    except urllib2.HTTPError, e:
        if e.code==404:
            interface.Reply("There is no wiki page for %s"%args)
            return
        else:
            interface.Reply("Error (%u) loading wiki page."%e.code)
            return

    doc = BeautifulSoup(response)
    t = doc.table
    if t: t.extract()

    defin = doc.find("p")
    o = FormatHTML(defin.renderContents())
    o = re.sub('\[[0-9]*?\]','',o)
    if len(o)>600: o=o[:597]+"..."
    title = re.search('<title>(.+?) - Wikipedia, the free encyclopedia</title>', response).group(1) #yoink

    return {'title':title,'content':o}


def WikiHandle(interface,command,args,messagetype):

    page = GetPage(args)
    o = ("%s: %s"%(page['title'],page['content'].decode('utf-8')))
    interface.Reply(o)


global game
game=None

def GameHint():
    global game
    r = re.sub(game['title'],'*THING*', game['content'],re.IGNORECASE)
    b = game['title'].partition(' (')[0]
    c = game['title'].partition(', ')[0]
    r = re.sub(b,'*THING*',r,re.IGNORECASE)
    r = re.sub(c,'*THING*',r,re.IGNORECASE)
    return r


def GuessWiki(interface,command,args,message):
    global game
    if game==None:
        game=GetPage()
        interface.Reply("Type %sguesswiki title to guess what this is!"%interface.GetPrefix())
        interface.Reply(GameHint())
    else:
        if args.strip()=='':
            interface.Reply("Type %sguesswiki title to guess what this is!"%interface.GetPrefix())
            interface.Reply(GameHint())
        elif args.lower()==game['title'].lower() or args.lower()==game['title'].partition(' (')[0].lower():
            interface.Reply("Correct!")
            #interface.Reply("%s: %s"%(game['title'],game['content']))
            game=None
        else:
            interface.Reply("Incorrect.")


interface.ComHook("wiki",WikiHandle,name="WikiBot")
interface.ComHook("guesswiki",GuessWiki,name="WikiGame")

"""

import interface
from BeautifulSoup import BeautifulSoup
from stringsafety import *
import urllib2


def Handle(interface,command,args,messagetype):
    !ud phrase - Look up a phrase on urban dictionary.
    url = "http://www.urbandictionary.com/"+escapeurl(args)
    response = urllib2.urlopen(url)
    doc = BeautifulSoup(response)
    defin = doc.find("div",{"class":"definition"})
    interface.Reply(args+" - "+FormatHTML(defin.renderContents()))

interface.ComHook('ud',Handle,name='UrbanBot')
"""