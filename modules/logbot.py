
import interface
import re

def Handle(it,text):
    # @type it ChatInterface
    f=None
    r = re.compile('[^\w]')

    filename = "data\\logs\\"+r.sub("",it.Message.ChatName)+".txt"
    try:
        f = open(filename,"a+")
    except:
        f = open(filename,"w")
        f.close()
        f = open(filename,"a+")
    f.write("[%s] %s: %s\n" % (it.Message.Datetime.strftime("%d/%m/%Y %H:%M:%S"),it.UserName,text))
    f.close()


interface.MessageHook(Handle)
