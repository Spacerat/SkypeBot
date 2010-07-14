
import interface
from BeautifulSoup import BeautifulSoup
from stringsafety import *
import urllib2


def Handle(interface,command,args,messagetype):
    """!ud phrase - Look up a phrase on urban dictionary."""
    url = "http://www.urbandictionary.com/"+escapeurl(args)
    response = urllib2.urlopen(url)
    doc = BeautifulSoup(response)
    defin = doc.find("div",{"class":"definition"})
    interface.Reply(args+" - "+FormatHTML(defin.renderContents()))

interface.ComHook('ud',Handle,name='UrbanBot')
