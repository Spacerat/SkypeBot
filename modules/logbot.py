
import interface

def Handle(interface,text):
    f = open("log.txt","a+")
    f.write(interface.UserName+"\n")
    f.write(interface.UserAddress+"\n")
    f.write(text+"\n")
    f.close()

    text = text.replace("\r\n\r\n<<< ","")

interface.MessageHook(Handle)
