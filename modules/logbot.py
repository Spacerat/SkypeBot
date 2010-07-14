
import interface
import re
import codecs

def Handle(it,text):
    # @type it ChatInterface
    f=None
    r = re.compile('[^\w]')

    filename = "data\\logs\\"+r.sub("",it.Message.ChatName)+".txt"
    try:
        f = codecs.open(filename,"a+","utf-8")
    except:
        f = open(filename,"w")
        f.close()
        #f = open(filename,"a+")
        f = codecs.open(filename,"a+","utf-8")
    
    m = "[%s] %s: %s\n" % (it.Message.Datetime.strftime("%d/%m/%Y %H:%M:%S"),it.UserName,text)
    #m=str(m)
    f.write(m)
    f.close()


interface.MessageHook(Handle)
