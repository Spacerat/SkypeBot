import modules.interface

from modules.interface import RecieveMessage, DebugInterface
import modules
modules.load_modules(open('data/modules.txt').readlines())
import threading

if __name__ == "__main__":
    print "Welcome to JoeBot! You can enter chatbot commands in this console."
    print "You probably want to run !skype, !msn, or !irc"
    cmd = '';
    while not cmd == 'exit':
        cmd = raw_input('>').decode('latin-1')
        threading.Thread(RecieveMessage(DebugInterface(),cmd,'SENT')).start()
