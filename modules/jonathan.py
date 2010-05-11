
import interface
from BeautifulSoup import BeautifulSoup
from stringsafety import *
import urllib2


def Handle(interface,command,args,messagetype):
    url = "http://jonathanfromspotifyruinedyourplaylist.com/"+escapeurl(args)
    response = urllib2.urlopen(url)
    doc = BeautifulSoup(response)
    defin = doc.find("a")
    interface.Reply(FormatHTML(defin.renderContents()))

interface.AddHook('jonathan',Handle,name='')
