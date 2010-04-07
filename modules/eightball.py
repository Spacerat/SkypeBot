
import robot
import random
import time

random.seed(time.time())

class EightBallRobot(robot.SkypeRobot):
    def OnInit(self):
        self.Name = "8Bot"
    def Handle(self,command,args):
        ballfile = open("data/8ball.txt")
        lines = ballfile.readlines()
        if not args.endswith("?"):
            args=args+"?"
        self.Reply(args+" "+lines[random.randint(0,len(lines)-1)])


robot.AddHook("8ball",EightBallRobot)
