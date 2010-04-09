# ----------------------------------------------------------------------------------------------------
#  Python / Skype4Py super Skype Bot

import Skype4Py
import modules.echo
import os.path

from modules.skype import SkypeInterface
from modules.interface import RecieveMessage
import modules.eightball
import modules.google
import modules.lastfm
import modules.define
import modules.feed


# ----------------------------------------------------------------------------------------------------
# Fired on attachment status change. Here used to re-attach this script to Skype in case attachment is lost. Just in case.
def OnAttach(status):
    print 'API attachment status: ' + skype.Convert.AttachmentStatusToText(status)
    if status == Skype4Py.apiAttachAvailable:
        skype.Attach();

    if status == Skype4Py.apiAttachSuccess:
       print('******************************************************************************');

# ----------------------------------------------------------------------------------------------------
# Fired on chat message status change.
# Statuses can be: 'UNKNOWN' 'SENDING' 'SENT' 'RECEIVED' 'READ'

def OnMessageStatus(Message, Status):
    RecieveMessage( SkypeInterface(Message,Status),Message.Body,Status )
    
# ----------------------------------------------------------------------------------------------------
# Creating instance of Skype object, assigning handler functions and attaching to Skype.
skype = Skype4Py.Skype()

skype.OnAttachmentStatus = OnAttach;
skype.OnMessageStatus = OnMessageStatus;
# ----------------------------------------------------------------------------------------------------
# Modules setup
modules.lastfm.SetAPIKey(open("data/lastFMAPIKey.txt").readline())
modules.define.SetToken(open("data/abbrtoken.txt").readline())
modules.feed.LoadFeedsJSON(os.path.abspath("data/feeds.txt"))

print('******************************************************************************');
print 'Connecting to Skype..'
skype.Attach()

# ----------------------------------------------------------------------------------------------------
# Looping until user types 'exit'
Cmd = '';
while not Cmd == 'exit':
    Cmd = raw_input('');
