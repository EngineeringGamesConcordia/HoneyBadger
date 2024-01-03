from arm import Arm
from drive import Drive
from relay import Relay
from time import sleep, time


class Automation:
    def __init__(self, arm, drive):
        self.arm = arm
        self.drive = drive
        print("Init automation")
        self.flipper = False;

    def start(self):       
        
        print("> automation start")
        print("Beginning driving")

        #Turn towards right
        t_end = time() + 0.5
        while time() > t_end:
            self.drive.move_right()
        self.drive.move_stop()
        

         #drive forward for X
        t_end = time() + 0.7
        while time() > t_end:
            self.drive.move_forward()
        self.drive.move_stop()      
        
        #This is trying to launch 
        for x in range (5):
            self.
            
            