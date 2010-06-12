import string

import interface
import re

class Hangman:

    def __init__(self,word,chances=8):
        self.word = word
        self.foundletters = ""
        self.wrongletters = ""
        self.chances=chances

    def GetCurrentGuess(self):
        guess = ""
        for x in self.word:
            if (x.lower() in self.foundletters) or (x in string.whitespace or x in string.punctuation):
                guess+=x
            else:
                guess+="*"
        return guess

    def GetWord(self):
        return self.word

    def GuessLetter(self,letter):
        if letter in self.foundletters:
            return 2 #alread found
        if letter in self.wrongletters:
            return -1 #already missed
        if letter.lower() in self.word.lower():
            self.foundletters+=letter.lower()
            return 1 #found
        else:
            self.UseChance()
            if len(letter)==1: self.wrongletters+=letter.lower()
            return 0 #missed
    def UseChance(self):
        self.chances-=1

def FailGame(interface):
    global currentgame
    interface.Reply("You have used up all of your chances. The word was "+currentgame.word)
    interface.Reply("You lose the game.")
    currentgame = None


def StartHangman(interface,command,args,messagetype):
    global currentgame
    try:
        if (currentgame!=None):
            interface.Reply("Hangman is already running!")
            return
    except:
        pass
    
    if args.strip()=="":
        interface.Reply("use %shangman word" % interface.GetPrefix())
        return
    if "*" in args:
        interface.Reply("The word must not contain *")
        return
    currentgame = Hangman(args)
    try:
        interface.Message.Body="HangBot: Time for a game of hangman!"
    except:
        return
        for x in range(30):
            interface.Reply("")
    interface.Reply("The word is "+currentgame.GetCurrentGuess())
    interface.Reply("Use %sguess <letter or word/phrase>, %sgetfails and %sgetword" % interface.GetPrefix())

def GuessHangman(interface,command,args,messagetype):
    global currentgame
    try:
        if not (currentgame):
            interface.Reply("There is no running game of Hangman.")
            return
    except:
        interface.Reply("There is no running game of Hangman.")
        return
    if currentgame.word.lower() == args.lower():
            interface.Reply("Correct! The word is "+currentgame.word+".")
            interface.Reply("End of game.")
            currentgame = None
    else:
        r = currentgame.GuessLetter(args)
        if  r >0:
            g = currentgame.GetCurrentGuess()
            if "*" in g:
                interface.Reply(args + " is in the word.")
                interface.Reply("The word is "+g)
            else:
                interface.Reply("Success! The word is "+g+".")
                interface.Reply("End of game.")
                currentgame = None
        elif r==0:
            if currentgame.chances==-1:
                FailGame(interface)
            else:
                interface.Reply(args + " is not in the word. You have "+str(currentgame.chances)+" chances left.")
                interface.Reply("The letters "+currentgame.wrongletters+" are not in the word.")
        elif r==-1:
            interface.Reply("You have already guessed "+args+" and it is not in the word.")

def GetFails(interface,command,args,messagetype):
    global currentgame
    try:
        if not (currentgame):
            interface.Reply("There is no running game of Hangman.")
            return
    except:
        interface.Reply("There is no running game of Hangman.")
        return
    interface.Reply(currentgame.wrongletters + " are not in the word.")

def GetWord(interface,command,args,messagetype):
    global currentgame
    try:
        if not (currentgame):
            interface.Reply("There is no running game of Hangman.")
            return
    except:
        interface.Reply("There is no running game of Hangman.")
        return
    interface.Reply("The word is "+currentgame.GetCurrentGuess())



interface.ComHook("hangman",StartHangman,"HangBot")
interface.ComHook("guess",GuessHangman,"HangBot")
interface.ComHook("getfails",GetFails,"HangBot")
interface.ComHook("getword", GetWord,"HangBot")
