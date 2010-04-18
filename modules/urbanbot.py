
import interface
from BeautifulSoup import BeautifulSoup
from stringsafety import *
import urllib2


def Handle(interface,command,args,messagetype):
    url = "http://www.urbandictionary.com/"+escapeurl(args)
    response = urllib2.urlopen(url)
    doc = BeautifulSoup(response)
    defin = doc.find("div",{"class":"definition"})
    interface.Reply(args+" - "+FormatHTML(defin.renderContents()))

interface.AddHook('ud',Handle,name='UrbanBot')