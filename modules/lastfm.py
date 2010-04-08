
import interface
from stringsafety import *

#-------LASTFM FUNCTIONS---------#
import urllib2
import json

def SetAPIKey(key):
    global keystring
    apikey = key
    keystring = "&api_key="+apikey

lastfmurl = "http://ws.audioscrobbler.com/2.0/?"
keystring=''
formatstring = "&format=json"
users = {"joe":"JoeAT","lulu":"azayii","louise":"lspiritFM","alex":"Socratesv1","sinead":"shinzo7","shinzo":"Shinzo7","ramon":"twilightlullaby","rammi":"twilightlullaby"}

def GetRecentTrack(User):
    url = lastfmurl+"method=user.getrecenttracks&user={0}{1}{2}".format(URLSafe(User),formatstring,keystring)
    request = urllib2.Request(url,None,{'Referer':'http://spacerat.meteornet.net'})
    response = urllib2.urlopen(request)
    results = json.load(response)
    
    if "recenttracks" in results:
        if "track" in results["recenttracks"]:
            track = results["recenttracks"]["track"][0]

            return track

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
                str = track["artist"]["#text"]+" - " + track["name"]
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

interface.AddHook("listening",Handle,"LastfmBot")
interface.AddHook("artist",Handle,"LastfmBot")

