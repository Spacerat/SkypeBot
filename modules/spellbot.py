
import interface
import urllib2
import json
from stringsafety import *

def SetYahooID(str):
    global id
    id = str

id=''

def Handle(interface,command,args,messagetype):
    if args.strip()=='':
        interface.Reply('Use !spell <word>')
        return

    url = "http://search.yahooapis.com/WebSearchService/V1/spellingSuggestion?appid={0}&output=json&query={1}".format(id,escapeurl(args))
    request = urllib2.Request(url,None,{'Referer':'http://spacerat.meteornet.net'})
    response={}
    try:
        response = urllib2.urlopen(request)
        data = json.load(response)
    except urllib2.HTTPError as e:
        interface.Reply('You caused a {0} error! (chuckle)'.format(e.code))
        return


    results = data.get('ResultSet',{})
    if 'Result' in results:
        interface.Reply(results['Result'].capitalize()+".")
    else:
        interface.Reply('No word found, or word already correct.')


interface.AddHook("spell",Handle,"SpellBot")
