
import robot

class EchoRobot(robot.SkypeRobot):
    def OnInit(self):
        self.Name = "EchoBot"
    def Handle(self,command,args):
        self.Reply(args)

robot.AddHook("echo",EchoRobot)
