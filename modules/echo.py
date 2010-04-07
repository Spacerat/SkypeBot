
import robot

class EchoRobot(robot.SkypeRobot):
    def Handle(self,command,args):
        self.Reply(args)

robot.AddHook("echo",EchoRobot)

print "added echo hook"
