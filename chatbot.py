
import skypebot
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
import modules.quotebot

import os.path

# ----------------------------------------------------------------------------------------------------
# Modules setup
modules.lastfm.SetAPIKey(open("data/lastFMAPIKey.txt").readline())
modules.lastfm.LoadUserAliases("data/lastfmalias.txt")
modules.define.SetToken(open("data/abbrtoken.txt").readline())
modules.feed.LoadFeedsJSON(os.path.abspath("data/feeds.txt"))
modules.spellbot.SetYahooID(open("data/yahooid.txt").readline())

if __name__ == "__main__":
    skypebot.Init(prefix="!")
    
    Cmd = '';
    while not Cmd == 'exit':
        Cmd = raw_input('>');
