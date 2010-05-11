
import interface
import urllib2
import json
import enchant
from enchant.tokenize import get_tokenizer, EmailFilter, URLFilter
from enchant.checker import SpellChecker
from stringsafety import *

d = enchant.Dict("en_UK")
tkn = get_tokenizer("en_UK",filters=[URLFilter,EmailFilter])

def SetYahooID(str):
    global id
    id = str

id=''

def Spell(word):

    if d.check(word)==True:
        return word
    else:
        return d.suggest(word)
    '''
    url = "http://search.yahooapis.com/WebSearchService/V1/spellingSuggestion?appid={0}&output=json&query={1}".format(id,escapeurl(word))
    request = urllib2.Request(url,None,{'Referer':'http://spacerat.meteornet.net'})
    response={}
    data = None
    try:
        response = urllib2.urlopen(request)
        data = json.load(response)
    except urllib2.HTTPError as e:
        pass

    if data:
        results = data.get('ResultSet',{})

        if 'Result' in results:
            return results['Result']
        else:return d.suggest(word)
        '''

def SpellBot(interface,command,args,messagetype,onlyerror=False):
    words=args
    if args.strip()=='':
        words = interface.LastMessages[0].Body
        onlyerror=True

    for word in tkn(words):
        w = Spell(word[0])
        if word[0] == w:
            if not onlyerror: interface.Reply(word[0]+" is spelt correctly.")
        elif w:
            interface.Reply(word[0]+": "+", ".join(w))
        else:
            interface.Reply(word[0]+" is unrecognisable.")

def CorrectBot(interface,command,args,messagetype):
    words=''
    chkr = SpellChecker("en_UK",filters=[EmailFilter,URLFilter])

    try:
        a=args.split()
        n=int(args.split()[0])
        if len(a)>1:
            words=args.partition(" ")[2]
        else:
            words=interface.LastMessages[n].Body
    except:
        n=0
        words=interface.LastMessages[0].Body

    if not interface.LastMessages[n].IsEditable:
        SpellBot(interface,'spell',words,messagetype,onlyerror=True)
        return

    text=interface.LastMessages[n].Body
    origtext = text

    chkr.set_text(words)
    for err in chkr:
        w = err.suggest()#Spell(word[0])
        if w:
            if w!=err.word:
                text = text.replace(err.word,w[0])

    if origtext!=text:
        interface.LastMessages[n].Body=text

interface.AddHook("spell",SpellBot,name="SpellBot")
interface.AddHook("correct",CorrectBot,name="SpellBot")
