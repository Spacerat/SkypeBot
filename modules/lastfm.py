
import interface
from stringsafety import *

#-------LASTFM FUNCTIONS---------#
import urllib2
import json

lastfmurl = "http://ws.audioscrobbler.com/2.0/?"
keystring=''
formatstring = "&format=json"
datafile = ''
users = {}

def SetAPIKey(key):
    global keystring
    apikey = key
    keystring = "&api_key="+apikey

def LoadUserAliases(url):
    global users
    global datafile
    f=open(url)
    if f:
        users = json.load(f)
        f.close()
        datafile = url

def ExportUserAliases(url=''):
    global datafile
    if url=='': url = datafile
    f = open(url,'w')
    if f: json.dump(users,f)

def GetRecentTrack(User):
    url = lastfmurl+"method=user.getrecenttracks&user={0}&limit=1{1}{2}".format(escapeurl(User),formatstring,keystring)
    request = urllib2.Request(url,None,{'Referer':'http://spacerat.meteornet.net'})
    response = urllib2.urlopen(request)
    results = json.load(response)
    
    if "recenttracks" in results:
        if "track" in results["recenttracks"]:

            if 'name' in results["recenttracks"]["track"]:
                return results["recenttracks"]["track"]
            else:
                return results["recenttracks"]["track"][0]

def GetArtistInfo(Artistname):
    url = lastfmurl+"method=artist.getinfo&artist={0}{1}{2}".format(escapeurl(Artistname),formatstring,keystring)
    request = urllib2.Request(url,None,{'Referer':'http://spacerat.meteornet.net'})
    response = urllib2.urlopen(request)
    results = json.load(response)
    return results
#-----------------------------------#

def Handle(interface,command,args,messagetype):
    edit = False
    if command == 'listening':
        names = args.split()
        if not names:
            names = [interface.UserAddress]
        if len(names)==1:
            edit=True
        
        for usr in names:
            try:
                if usr.lower() in users: usr = users[usr.lower()]
            except Exception as e:
                print repr(e)
                return
            track = GetRecentTrack(usr)
            if track:
                str = track["artist"]["#text"]+" - "+track["name"]
                current = ""
                if "@attr" in track:
                    current = " is currently playing: "
                else:
                    current = " last played: "

                interface.Reply(usr+current +str)#,edit=edit)
            else:
                interface.Reply(usr+" has never listened to anything. Ever. :(",edit=edit)
    elif command == 'artist':
        info = GetArtistInfo(args)
        if info:
            content = info['artist']['bio']['content']
            artisturl = info['artist']['url']
            interface.Reply(artisturl)
            interface.Reply(FormatHTML(content)[0:400]+" ...")

def AddUsrHandle(interface,command,args,messagetype):
    if len(args.split())==2:
        if args.split()[0].lower() in users:
            interface.Reply('Cannot overwrite existing user '+args.split()[0])
            return
        User = args.split()[1]
        url = lastfmurl+"method=user.getinfo&user={0}{1}{2}".format(escapeurl(User),formatstring,keystring)
        request = urllib2.Request(url,None)
        response = urllib2.urlopen(request)
        results = json.load(response)
        if 'user' in results:
            users[args.split()[0].lower()] = User
            ExportUserAliases()
            Handle(interface,'listening',User,messagetype)
    else:
        interface.Reply('use %saddfm Alias Username' % interface.GetPrefix())

def ListFMHandle(interface,command,args,messagetype):
    interface.Reply(", ".join(users))

interface.ComHook("listening",Handle,name="LastfmBot")
interface.ComHook("artist",Handle,name="LastfmBot")
interface.ComHook("addfm",AddUsrHandle,name="LastfmBot")
interface.ComHook("listfm",ListFMHandle,name="LastfmBot")
