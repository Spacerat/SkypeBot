
import skrobot

class EchoRobot(skrobot.SkypeRobot):
    def OnInit(self):
        self.Name = "EchoBot"
    def Handle(self,command,args):
        self.Reply(args)

skrobot.AddHook("echo",EchoRobot)
