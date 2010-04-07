
import robot
from stringsafety import *

#-------LASTFM FUNCTIONS---------#
import urllib2
import json


lastfmurl = "http://ws.audioscrobbler.com/2.0/?"
apikey = "f88d0775a11b5d05fcbd1cc4b75b4314"
keystring = "&api_key="+apikey
formatstring = "&format=json"
users = {"Joe":"JoeAT","Lulu":"azayii","Louise":"lspirit","Alex":"Socratesv1","Sinead":"Shinzo7","Shinzo":"Shinzo7","Ramon":"twilightlullaby","Rammi":"twilightlullaby"}

def GetRecentTrack(User):
    url = lastfmurl+"method=user.getrecenttracks&user="+URLSafe(User)+formatstring+keystring
    request = urllib2.Request(url,None,{'Referer':'http://spacerat.meteornet.net'})
    response = urllib2.urlopen(request)
    results = json.load(response)
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

class LastFMRobot(robot.SkypeRobot):
    def OnInit(self):
        self.Name = "LastFMBot"
    def Handle(self,command,args):
        if command == 'listening':
            names = args.split()
            for usr in names:
                if usr in users: usr = users[usr]
                track = GetRecentTrack(usr)
                if track:
                    str = track["artist"]["#text"]+" - " + track["name"]
                    current = ""
                    if "@attr" in track:
                        current = " is currently playing: "
                    else:
                        current = " last played: "

                    self.Reply(usr+current +str)
                else:
                    self.Reply(usr+" has never listened to anything. Ever. :(")
        elif command == 'artist':
            info = GetArtistInfo(args)
            if info:
                content = info['artist']['bio']['content']
                artisturl = info['artist']['url']
                self.Reply(artisturl)
                self.Reply(FormatHTML(content)[0:400]+" ...")

robot.AddHook("listening",LastFMRobot)
robot.AddHook("artist",LastFMRobot)