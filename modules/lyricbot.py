
import interface
from xml.dom import minidom
from stringsafety import *
import urllib2

def SearchLyricText(callback,text,includeurl=False):
    url=r'http://api.chartlyrics.com/apiv1.asmx/SearchLyricText?lyricText='+escapeurl(text)
    request = urllib2.Request(url,None,{'Referer':'http://spacerat.meteornet.net'})
    response = urllib2.urlopen(request)
    data = minidom.parse(response)

    artist =  data.getElementsByTagName("Artist")[0].firstChild.data
    title =  data.getElementsByTagName("Song")[0].firstChild.data
    
    callback(artist+" - "+title)
    
    if includeurl:
        url = data.getElementsByTagName("SongUrl")[0].firstChild.data
        callback(url)

def Handle(interface,command,args,messagetype):
    if args.strip()=='':
        interface.Reply('use !findsong <lyrics>')
    else:
        SearchLyricText(interface.Reply, args)
    
interface.AddHook('findsong',Handle,'LyricBot')
