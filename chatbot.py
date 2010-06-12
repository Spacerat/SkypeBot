
import msnbot
import skypebot
import irc

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
#import modules.logbot
import modules.skype
import modules.interface

import threading

import os.path

# ----------------------------------------------------------------------------------------------------
# Modules setup
modules.lastfm.SetAPIKey(open("data/lastFMAPIKey.txt").readline())
modules.lastfm.LoadUserAliases("data/lastfmalias.txt")
modules.quotebot.LoadUserAliases("data/skypealias.txt")
modules.define.SetToken(open("data/abbrtoken.txt").readline())
modules.feed.LoadFeedsJSON(os.path.abspath("data/feeds.txt"))
modules.spellbot.SetYahooID(open("data/yahooid.txt").readline())
modules.correctbot.LoadReplaceDict("data/repdict.txt")
modules.scheduler.AddInterface(modules.interface.DebugInterface())



if __name__ == "__main__":
    #skypebot.Init()
    
    Cmd = '';
    while not Cmd == 'exit':
        Cmd = raw_input('>');
        if Cmd=='msn':
            modules.interface.SetPrefix("!")
            threading.Thread(None,msnbot.init).start()
        elif Cmd=='irc':
            modules.interface.SetPrefix(".")
            irc.IRC(irc.Network(server='irc.calculasm.org',nick='JoeBot',ident='joebot',realname="Joe's bot",channels=["#mudkipz"] )).start()
        elif Cmd=='skype':
            modules.interface.SetPrefix("!")
            skypebot.Init()
