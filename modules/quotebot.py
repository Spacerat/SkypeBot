
import MySQLdb
import re
import interface
import json
import datetime


def ProcessDateFormat(dt,inputsep="/",outputsep="-"):
    if dt == None or dt=="": return datetime.date.today().isoformat()
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

    db = MySQLdb.connect(dbinfo['host'],
                         dbinfo['user'],
                         dbinfo['pwd'],
                         dbinfo['db'],use_unicode=True)

    db.set_character_set('utf8')
    c = db.cursor()
    c.execute('SET NAMES utf8')
    c.execute('SET character_set_connection=utf8')
    c.execute('SET CHARACTER SET utf8')

    return db

def CreateTables(db=None, drop=False):

    if db==None:
        conn = GetConnection()
    else:
        conn=db

    cursor = conn.cursor()
    if drop: cursor.execute("DROP TABLE quotes")
    if drop: cursor.execute("DROP TABLE handles")
    cursor.execute("""
        CREATE TABLE quotes
        (
        id          MEDIUMINT UNSIGNED NOT NULL AUTO_INCREMENT,
        text        TEXT,
        timestamp   TIMESTAMP,
        client      CHAR(5),
        rating      INT,
        PRIMARY KEY(id)
        )
    """)
    cursor.execute("""
        CREATE TABLE handles
        (
        id          MEDIUMINT UNSIGNED NOT NULL,
        handle      VARCHAR(32),
        FOREIGN KEY (id) REFERENCES quotes(id),
        PRIMARY KEY (id, handle)
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
    r.execute("SELECT text FROM quotes ORDER BY timestamp")
    ret=""
    for x in r.fetchall():
        ret=ret+"\n"+x[0]

    interface.Reply(ret)

    c.close()

def AddQuote(quote,db=None):

    if db==None:
        conn = GetConnection()
    else:
        conn=db

    cursor = conn.cursor()
    text = conn.escape_string(quote['text'].encode('utf-8')).decode('utf-8')
    timestamp = quote['timestamp']
    client = conn.escape_string(quote['client'])
    query="INSERT INTO quotes (text,timestamp,client,rating) VALUES ('%s', '%s', '%s', %u)"%(text, timestamp, client,0)
    query = query.encode('utf-8')
    cursor.execute(query)
    id=cursor.lastrowid
    for h in quote['handles']:
        cursor.execute("INSERT INTO handles VALUES (%u, '%s')"%(id,conn.escape_string(h)))

    conn.commit()
    if db==None: conn.close()
    return True


def GetQuoteByString(search,n=1,db=None):
    if db==None:
        conn = GetConnection()
    else:
        conn=db

    cursor=conn.cursor()
    search = conn.escape_string(search)

    cursor.execute("""
        SELECT text
        FROM quotes
        WHERE text RLIKE ('%s')
        ORDER BY RAND()
        LIMIT %u
    """%(search,n))

    return cursor.fetchall()

def GetQuoteByHandle(handle=None,n=1,db=None):
    if db==None:
        conn = GetConnection()
    else:
        conn=db

    cursor = conn.cursor()
    handle=conn.escape_string(handle)

    cursor.execute("""
        SELECT text
        FROM quotes
        WHERE id IN
            (SELECT id FROM handles WHERE handle = '%s')
        ORDER BY RAND()
        LIMIT %u

    """%(handle,n))

    return cursor.fetchall()

def Handle(interface,command,args,messagetype):
    global aliases
    if args.strip()=="":
        '''
        interface.ReplyToSender("To add a quote: copy the quote, then type %squote and paste your quote."%interface.GetPrefix())
        interface.ReplyToSender("To retrieve a quote: Type %squote search-string)
        interface.ReplyToSender("When using the quotebot, user names must either be the nicknames currently in use, or in the alias list.")
        '''
        q=GetQuote()
        interface.Reply("\n"+q)
        return

    if interface.Type == "Skype":

        regexp=r"^\[(\d\d/\d\d/\d\d\d\d )*(\d\d:\d\d:\d\d)( \| )*(Edited .*)*\] (.*?): (.*?)$" #Fuck yeah

        lines = re.findall(regexp,args,re.M)
        
        
        if len(lines)>0:
            quotedict={}
            quotedict['timestamp']=ProcessDateFormat(lines[0][0])+" "+lines[0][1]
            quotedict['text']=args
            quotedict['client']='Skype'
            quotedict['handles']=[]

            print quotedict['timestamp']

            for line in lines:
                name = line[4]
                handle=""
                try:
                    handle = interface.Users.get(name,aliases[name.lower()])
                except:
                    interface.Reply("No skype handle found for %s. Please change the name in the quote to %s's current nickname." % (name,name))
                    return
                if not handle in quotedict['handles']: quotedict['handles'].append(handle)

            if AddQuote(quotedict):
                interface.Reply("Quote added!")

        else:
            q=None
            handle = interface.Users.get(args,aliases.get(args.lower()))
            if handle==None:
                q=GetQuoteByString(args)
            else:
                q=GetQuoteByHandle(handle)

            if q==None or len(q)==0:
                interface.Reply("No quotes stored for "+args)
                return
            interface.Reply("\n"+q[0][0])


interface.ComHook("quote",Handle,name='QuoteBot')
interface.ComHook("resetquotes",ResetQuotes,hidden=True,status='SENT',name='QuoteBot')
interface.ComHook("getallquotes",GetAllQuotes,hidden=True,status='SENT',name='QuoteBot')
