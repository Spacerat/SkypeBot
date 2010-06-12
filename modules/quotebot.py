
import MySQLdb
import re
import interface
import json
from random import randint

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

def CreateTables(db=None):
    if db==None:
        conn = GetConnection()
    else:
        conn=db
    cursor = conn.cursor()
    cursor.execute("DROP TABLE quotes")
    cursor.execute("""
        CREATE TABLE quotes
        (
        handle      CHAR(20),
        text        TEXT,
        timestamp   CHAR(20),
        groupid     SMALLINT UNSIGNED,
        client      CHAR(10)
        )
    """)

    cursor.close()
    if db==None: conn.close()

def ResetQuotes(interface,command,args,messagetype):
    CreateTables()
    interface.Reply("Done.")

def GetAllQuotes(interface,command,args,messagetype):
    c = GetConnection()
    r = c.cursor()
    r.execute("SELECT * FROM quotes")

    for x in r.fetchall():
        interface.ReplyToSender(x[1])
        
    c.close()

#Accepts a list of dictionaries, containing 'handle', 'text', and 'timestamp' keys.
def AddQuote(quotes,db=None):

    if db==None:
        conn = GetConnection()
    else:
        conn=db

    if len(quotes)>1:
        gcursor=conn.cursor()
        gcursor.execute("SELECT MAX(groupid) FROM quotes")

        group = int(gcursor.fetchone()[0])+1
        gcursor.close()

    else:
        group = 0

    cursor = conn.cursor()
    
    for quote in quotes:
        text = conn.escape_string(quote['text'])
        handle = conn.escape_string(quote['handle'])
        timestamp = conn.escape_string(quote['timestamp'])
        client = conn.escape_string(quote['client'])

        cursor.execute("INSERT INTO quotes VALUES ('%s', '%s', '%s', '%u', '%s')"%(handle, text, timestamp, group, client))

    conn.commit()
    if db==None: conn.close()
    return True

def GetQuote(handle,db=None):
    if db==None:
        conn = GetConnection()
    else:
        conn=db

    cursor = conn.cursor()

    r=[]
    cursor.execute("SELECT text,groupid,timestamp FROM quotes WHERE handle = '%s'" % handle)
    rows=cursor.fetchall()

    if not rows: return None

    rownum = randint(0,len(rows)-1)
    row = rows[rownum]
    if row[1]>0:
        cursor.execute("SELECT text,timestamp FROM quotes WHERE groupid = %u"%row[1])
        multiquotes=cursor.fetchall()
        for multiquote in multiquotes:
            r.append("[%s] %s"%(multiquote[1],multiquote[0]))
    else:
        r.append("[%s] %s"%(row[2],row[0]))

    if db==None: conn.close()

    return r

def Handle(interface,command,args,messagetype):
    global aliases

    if interface.Type == "Skype":

        regexp=r"^\[(\d\d/\d\d/\d\d\d\d )*(\d\d:\d\d:\d\d)( \| )*(Edited .*)*\] (.*?): (.*?)$" #Fuck yeah

        quotes = re.findall(regexp,args,re.M)

        if len(quotes)>0:
            quotelist=[]

            for quote in quotes:
                quotedict = {}
                date = quote[0]
                time = quote[1]
                edit = quote[3]
                name = quote[4]
                text = quote[4]+": "+quote[5]
                try:
                    handle = interface.Users.get(name,aliases[name.lower()])
                except:
                    interface.Reply("No skype handle found for %s. Please change the name in the quote to %s's current nickname." % (name,name))
                    return

                quotedict['name']=name
                quotedict['time']=time
                quotedict['date']=date
                quotedict['timestamp']=time+" "+date
                quotedict['text']=text
                quotedict['edit']=edit
                quotedict['handle']=handle
                quotedict['client']="Skype"
                quotelist.append(quotedict)

            if AddQuote(quotelist):
                interface.Reply("Quote added!")

        else:
            try:
                handle = interface.Users.get(args,aliases[args.lower()])
            except:
                interface.Reply("No skype handle found for %s. Please change the name in the quote to %s's current nickname." % (args,args))
                return
            q = GetQuote(handle)
            if len(q)==0:
                interface.Reply("No quotes stored for "+args)
                return
            interface.Reply("\n"+"\n".join(q))


    '''
    else:
        nick = args
        try:
            handle = interface.Users[nick]
        except:
            
            return
        
        cursor.execute("SELECT user_name,text,datetime FROM quotes WHERE user_handle = '%s'" % handle)
        rows=cursor.fetchall()
        if not rows:
            interface.Reply("No quotes stored for "+nick)
            return

        row = rows[randint(0,len(rows)-1)]

        if row:
            interface.Reply("[%s] %s: %s"% (row[2],row[0],row[1]))
        conn.commit()

    conn.close()
    '''

interface.ComHook("quote",Handle,name='QuoteBot')
interface.ComHook("resetquotes",ResetQuotes,hidden=True,status='SENT',name='QuoteBot')
interface.ComHook("getallquotes",GetAllQuotes,hidden=True,status='SENT',name='QuoteBot')
