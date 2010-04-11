
import skypebot
import modules.echo
import modules.eightball
import modules.google
import modules.lastfm
import modules.define
import modules.feed
import modules.rimshot
import os.path

# ----------------------------------------------------------------------------------------------------
# Modules setup
modules.lastfm.SetAPIKey(open("data/lastFMAPIKey.txt").readline())
modules.lastfm.LoadUserAliases("data/lastfmalias.txt")
modules.define.SetToken(open("data/abbrtoken.txt").readline())
modules.feed.LoadFeedsJSON(os.path.abspath("data/feeds.txt"))


if __name__ == "__main__":
    skypebot.Init()
    
    Cmd = '';
    while not Cmd == 'exit':
        Cmd = raw_input('>');
