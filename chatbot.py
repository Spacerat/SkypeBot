
import msnbot
import skypebot
import irc


from modules.interface import RecieveMessage, DebugInterface, ComHook

import modules.echo
import modules.eightball
import modules.google
import modules.lastfm
import modules.define
import modules.feed
import modules.sillysites
import modules.lyricbot
import modules.spellbot
import modules.urbanbot
import modules.rhymebot #breaks everything when it fails. D:
import modules.eval
import modules.dice
import modules.correctbot
import modules.fortunebot
import modules.quotebot
import modules.jonathan
import modules.scheduler
import modules.hangman
import modules.logbot
import modules.skype
import modules.animbot
import modules.clearmessages
import modules.rot13bot
import modules.convokill
import modules.skypeadmin
import modules.securitycommands
import modules.security
import modules.omeglebot
import modules.wikibot

import threading

import os.path

import sys


# ----------------------------------------------------------------------------------------------------
# Modules setup
modules.lastfm.SetAPIKey(open("data/lastFMAPIKey.txt").readline())
modules.lastfm.LoadUserAliases("data/lastfmalias.txt")
modules.quotebot.LoadUserAliases("data/skypealias.txt")
modules.quotebot.LoadDBInfo("data/quotedb.txt")
modules.define.SetToken(open("data/abbrtoken.txt").readline())
modules.feed.LoadFeedsJSON(os.path.abspath("data/feeds.txt"))
modules.spellbot.SetYahooID(open("data/yahooid.txt").readline())
modules.correctbot.LoadReplaceDict("data/repdict.txt")
modules.scheduler.AddInterface(modules.interface.DebugInterface())
modules.convokill.LoadData("data/convokill.txt")
modules.security.LoadData("data/access.txt")


def StartSkype(i=None,command=None,args=None,messagetype=None):
    """!skype Start the skype bot"""
    skypebot.Init()
def StartMSN(i=None,command=None,args=None,messagetype=None):
    """!startmsn Start the msn bot"""
    threading.Thread(None,msnbot.init).start()

def StartIRC(i=None,command=None,args=None,messagetype=None):
    args=args.split()
    irc.IRC(irc.Network(server=args[0],nick='SpaceBot',ident='spacebot',realname="SpaceBot",channels=[args[1]] )).start()

ComHook('skype',StartSkype,security=4)
ComHook('msn',StartMSN,security=4)
ComHook('irc',StartIRC,security=4)

if __name__ == "__main__":
    #skypebot.Init()
    
    cmd = '';
    while not cmd == 'exit':
        cmd = raw_input('>').decode('latin-1');
        #try:
        threading.Thread(RecieveMessage(DebugInterface(),cmd,'SENT')).start()
        #except Exception as s:
        #    print str(s)

        '''
        if Cmd=='msn':
            threading.Thread(None,msnbot.init).start()
        elif Cmd=='irc':
            irc.IRC(irc.Network(server='irc.blitzed.org',nick='SpaceBot',ident='spacebot',realname="SpaceBot",channels=["#blitzbasic"] )).start()
        elif Cmd=='skype':
            skypebot.Init()
        '''
