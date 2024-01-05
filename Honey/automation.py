from arm import Arm
from drive import Drive
from relay import Relay
from time import sleep, time


class Automation:
    def __init__(self, arm, drive,relay):
        self.arm = arm
        self.drive = drive
        print("Init automation")
        self.flipper = False
        self.relay = relay

    def start(self):       
        self.flipper = False
        print("> automation start")
        print("Beginning driving")

        #Turn towards right
        t_end = time() + 5
        while time() < t_end:
            self.drive.move_right(1)
        self.drive.move_stop()
        

        #drive forward for X
        t_end = time() + 7
        while time() < t_end:
            self.drive.move_forward(1)
        self.drive.move_stop()          
        
        #This is trying to launch 
        for x in range (5):
            #run ball postion
            print("Auto Ball Position")
            self.arm.defaultPosition()
            sleep(3)
            self.arm.stepper_servo = 50
            self.arm.kit.servo[0].angle = self.arm.stepper_servo                  
            sleep(3)
            self.relay.start_vacuum()
            self.arm.ballPosition()
            
        #sweep arm
            self.arm.stepper_servo = self.arm.stepper_servo +x*10
            self.arm.kit.servo[0].angle = self.arm.stepper_servo  
            self.relay.start_throw()
            
            print("Auto Launch Position")
            self.arm.defaultPosition()
            sleep(3)
            self.arm.stepper_servo  = 125
            self.arm.kit.servo[0].angle = self.arm.stepper_servo
            sleep(3)
            self.arm.launchPosition()
            self.relay.stop_vacuum()