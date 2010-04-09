# ----------------------------------------------------------------------------------------------------
#  Python / Skype4Py super Skype Bot

import Skype4Py

from modules.skype import SkypeInterface
from modules.interface import RecieveMessage

skype = Skype4Py.Skype()

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

def Init():
    skype.OnAttachmentStatus = OnAttach;
    skype.OnMessageStatus = OnMessageStatus;


    print('******************************************************************************');
    print 'Connecting to Skype..'
    skype.Attach()

# ----------------------------------------------------------------------------------------------------
# Looping until user types 'exit'
if __name__ == "__main__":
    Cmd = '';
    Init()
    while not Cmd == 'exit':
        Cmd = raw_input('');
