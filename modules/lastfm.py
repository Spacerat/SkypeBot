
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
    url = lastfmurl+"method=user.getrecenttracks&user={0}{1}{2}".format(URLSafe(User),formatstring,keystring)
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
    url = lastfmurl+"method=artist.getinfo&artist={0}{1}{2}".format(URLSafe(Artistname),formatstring,keystring)
    request = urllib2.Request(url,None,{'Referer':'http://spacerat.meteornet.net'})
    response = urllib2.urlopen(request)
    results = json.load(response)
    return results
#-----------------------------------#

def Handle(interface,command,args,messagetype):
    if command == 'listening':
        names = args.split()
        for usr in names:
            if usr.lower() in users: usr = users[usr.lower()]
            track = GetRecentTrack(usr)
            if track:
                str = track["artist"]["#text"]+" - "+track["name"]
                current = ""
                if "@attr" in track:
                    current = " is currently playing: "
                else:
                    current = " last played: "

                interface.Reply(usr+current +str)
            else:
                interface.Reply(usr+" has never listened to anything. Ever. :(")
    elif command == 'artist':
        info = GetArtistInfo(args)
        if info:
            content = info['artist']['bio']['content']
            artisturl = info['artist']['url']
            interface.Reply(artisturl)
            interface.Reply(FormatHTML(content)[0:400]+" ...")

def AddUsrHandle(interface,command,args,messagetype):
    if len(args.split())==2:
        User = args.split()[1]
        url = lastfmurl+"method=user.getinfo&user={0}{1}{2}".format(URLSafe(User),formatstring,keystring)
        request = urllib2.Request(url,None)
        response = urllib2.urlopen(request)
        results = json.load(response)
        if 'user' in results:
            users[args.split()[0].lower()]
            ExportUserAliases()
            Handle(interface,'listening',User,messagetype)
    else:
        interface.Reply('use !addfm Alias Username')

interface.AddHook("listening",Handle,"LastfmBot")
interface.AddHook("artist",Handle,"LastfmBot")
interface.AddHook("addfm",AddUsrHandle,"LastfmBot")

