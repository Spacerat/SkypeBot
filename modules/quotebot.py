
import MySQLdb
import re
import interface
import json
import datetime
from random import randint


def SwapDateFormat(dt,inputsep="/",outputsep="-"):
    if dt == None or dt=="": return None
    dt=dt.strip()
    dt = dt.split(inputsep)
    return dt[2]+outputsep+dt[1]+outputsep+dt[0]

def LoadUserAliases(url):
    
    global aliases

    f=open(url)
    if f:
        aliases = json.load(f)
        f.close()
        datafile = url
    
def LoadDBInfo(url):

    global dbinfo
    dbinfo={}
    f=open(url)
    r=f.readlines()
    dbinfo['host']=r[0].rstrip()
    dbinfo['user']=r[1].rstrip()
    dbinfo['pwd']=r[2].rstrip()
    dbinfo['db']=r[3].rstrip()

def GetConnection():
    global dbinfo

    return MySQLdb.connect(dbinfo['host'],
                         dbinfo['user'],
                         dbinfo['pwd'],
                         dbinfo['db'])

def CreateTables(db=None, drop=False):

    if db==None:
        conn = GetConnection()
    else:
        conn=db

    cursor = conn.cursor()
    if drop: cursor.execute("DROP TABLE quotes")
    cursor.execute("""
        CREATE TABLE quotes
        (
        handle      TEXT,
        text        TEXT,
        timestamp   TIMESTAMP,
        groupid     SMALLINT UNSIGNED,
        client      CHAR(10)
        )
    """)

    cursor.close()
    if db==None: conn.close()

def ResetQuotes(interface,command,args,messagetype):
    if args=="drop":
        drop=True
    else:
        drop=False
    CreateTables(drop=drop)
    interface.Reply("Done.")

def GetAllQuotes(interface,command,args,messagetype):
    c = GetConnection()
    r = c.cursor()
    r.execute("SELECT * FROM quotes")

    for x in r.fetchall():
        interface.ReplyToSender("[%s] %s"%(x[2],x[1]))
        
    c.close()

#Accepts a list of dictionaries, containing 'handle', 'text', and 'timestamp' keys.
def AddQuote(quotes,db=None):

    if db==None:
        conn = GetConnection()
    else:
        conn=db

    gcursor=conn.cursor()
    gcursor.execute("SELECT MAX(groupid) FROM quotes")

    try:
        group = int(gcursor.fetchone()[0])+1
    except:
        group = 0

    gcursor.close()

    cursor = conn.cursor()
    
    for quote in quotes:
        text = conn.escape_string(quote['text'])
        handle = conn.escape_string(quote['handle'])
        timestamp = quote['timestamp']
        client = conn.escape_string(quote['client'])
        print timestamp
        cursor.execute("INSERT INTO quotes VALUES ('%s', '%s', '%s', '%u', '%s')"%(handle, text, timestamp, group, client))

    conn.commit()
    if db==None: conn.close()
    return True

def GetQuote(handle=None,search=None,db=None):
    if db==None:
        conn = GetConnection()
    else:
        conn=db

    cursor = conn.cursor()
    
    if handle==None or handle=="":
        handlestring=""
    else:
        handlestring="WHERE handle = '%s'"%handle
        
    if search==None or search=="":
        searchstring=""
    else:
        search = conn.escape_string(search)
        searchstring = "text RLIKE '(%s)'"%search
        if handle==None or handle=="":
            searchstring = "WHERE "+searchstring
        else:
            searchstring = "AND "+searchstring

    cursor.execute("""
    SELECT groupid
    FROM quotes
    %s
    %s
    GROUP BY groupid
    ORDER BY RAND()
    LIMIT 1
    """%(handlestring,searchstring))

    id = cursor.fetchone()
    if id==None:
        return
    else:
        id=id[0]

    cursor.execute("""
    SELECT timestamp,GROUP_CONCAT(text SEPARATOR '')
    FROM quotes
    WHERE groupid = %u
    GROUP BY groupid
    """%id)

    quote = cursor.fetchone()
    return quote[1]

def Handle(interface,command,args,messagetype):
    global aliases
    if args.strip()=="":
        '''
        interface.ReplyToSender("To add a quote: copy the quote, then type %squote and paste your quote."%interface.GetPrefix())
        interface.ReplyToSender("To retrieve a quote: Type %squote user. Optionally, add -> search_string."%interface.GetPrefix())
        interface.ReplyToSender("When using the quotebot, user names must either be the nicknames currently in use, or in the alias list.")
        '''
        q=GetQuote()
        interface.Reply("\n"+q)
        return

    if interface.Type == "Skype":

        regexp=r"^\[(\d\d/\d\d/\d\d\d\d )*(\d\d:\d\d:\d\d)( \| )*(Edited .*)*\] (.*?): (.*?)$" #Fuck yeah

        quotes = re.findall(regexp,args,re.M)

        if len(quotes)>0:
            quotelist=[]

            for quote in quotes:
                quotedict = {}
                date = quote[0]
                date = SwapDateFormat(date)
                time = quote[1]
                edit = quote[3]
                name = quote[4]
                text = quote[4]+": "+quote[5]
                try:
                    handle = interface.Users.get(name,aliases[name.lower()])
                except:
                    interface.Reply("No skype handle found for %s. Please change the name in the quote to %s's current nickname." % (name,name))
                    return

                if date==None:
                    date = datetime.date.today().isoformat()

                quotedict['name']=name
                quotedict['time']=time
                quotedict['date']=date
                quotedict['timestamp']=date+" "+time
                quotedict['text']=text
                quotedict['edit']=edit
                quotedict['handle']=handle
                quotedict['client']="Skype"
                quotelist.append(quotedict)

            if AddQuote(quotelist):
                interface.Reply("Quote added!")

        else:
            search=""
            if "->" in args:
                search = args.split("->")[1].strip()
                args = args.split("->")[0].strip()
            
            handle = interface.Users.get(args,aliases.get(args.lower()))
            if handle==None: search = args
            q = GetQuote(handle,search)
            if q==None:
                interface.Reply("No quotes stored for "+args)
                return
            interface.Reply("\n"+q)


interface.ComHook("quote",Handle,name='QuoteBot')
interface.ComHook("resetquotes",ResetQuotes,hidden=True,status='SENT',name='QuoteBot')
interface.ComHook("getallquotes",GetAllQuotes,hidden=True,status='SENT',name='QuoteBot')
