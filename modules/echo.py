
import robot

class EchoRobot(robot.SkypeRobot):
    def Handle(self,command,args):
        Reply(args)

modules.Hooks["echo"]=EchoRobot

print "added echo hook"
