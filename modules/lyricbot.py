
import interface
from xml.dom import minidom
from stringsafety import *
import urllib2

def SearchLyricText(callback,text,includeurl=False):
    url=r'http://api.chartlyrics.com/apiv1.asmx/SearchLyricText?lyricText='+escapeurl(text)
    request = urllib2.Request(url,None,{'Referer':'http://spacerat.meteornet.net'})
    try:
        response = urllib2.urlopen(request)
    except urllib2.HTTPError as e:
        if e.code==500:
            callback("You just caused an internal server error! (chuckle)")
        else:
            callback("You just caused a " + str(e.code)+ "internal server error! (chuckle)")
        return
    
    data = minidom.parse(response)

    if not data.getElementsByTagName("Artist"):
        callback('No song found.')
        return
    
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
    
interface.ComHook('findsong',Handle,name='LyricBot')
