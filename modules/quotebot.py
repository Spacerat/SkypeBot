
import MySQLdb
import re
import interface
import json
import datetime


def ProcessDateFormat(dt,inputsep="/",outputsep="-",swapdm=True):
    if dt == None or dt=="": return datetime.date.today().isoformat()
    dt=dt.strip()
    dt = dt.split(inputsep)
    if len(dt[1])==1: dt[1]="0"+dt[1]
    if len(dt[0])==1: dt[0]="0"+dt[0]
    if swapdm:
        return dt[2]+outputsep+dt[0]+outputsep+dt[1]
    else:
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

        #regexp=r"^\[(\d\d/\d\d/\d\d\d\d )*(\d\d:\d\d:\d\d)( \| )*(Edited .*)*\] (.*?): (.*?)$" #Fuck yeah

        regexp=r"^\[(.*?)\] ((.*?:)|(\*\*\*)) (.*?)$"

        lines = re.findall(regexp,args,re.M)

        if len(lines)>0:
            timestamp = lines[0][0].partition(" | ")[0]
            ts = timestamp.split()
            time=""
            date=None
            twelvehour=False
            if ts[len(ts)-1]=="PM":
                spl=ts[len(ts)-2].split(":")
                hour = int(spl[0])+12
                time=str(hour)+":"+spl[1]+":"+spl[2]
                twelvehour=True
            elif ts[len(ts)-1]=="AM":
                time=ts[len(ts)-2]
                twelvehour=True
            else:
                time=ts[len(ts)-1]
            if twelvehour and len(ts)==3:
                date=ts[len(ts)-3]
                date = ProcessDateFormat(date,"/","-",True)
            elif not twelvehour and len(ts)==2:
                date=ts[len(ts)-2]
                date = ProcessDateFormat(date,"/","-",False)
            else:
                date=None
                date = ProcessDateFormat(date)

            quotedict={}
            quotedict['timestamp']=date+" "+time
            quotedict['text']=args
            quotedict['client']='Skype'
            quotedict['handles']=[]

            print quotedict['timestamp']

            for line in lines:
                if len(line[4])>0: continue
                name = line[2]
                handle=""
                try:
                    handle = interface.Users.get(name,aliases[name.lower()])
                except:
                    pass
                if handle:
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
