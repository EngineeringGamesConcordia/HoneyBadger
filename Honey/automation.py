from arm import Arm
from drive import Drive
from vacuum import Vacuum
from motors import dcMotor
from time import sleep, time

class Automation:
    print("THIS IS HONEY")
    def __init__(self, arm, drive):
        self.arm = arm
        self.drive = drive
        print("Init automation")
        
    def start(self):
        print("> automation start")
        #Badger sets down Honey
        #Servo3 (wrist       up an amount
        t_end = time() + 0.5 #5 is second amount the wrist will go up
        while time() > t_end:
            self.arm.go_up() #arm.go_down()
            sleep(0.001)
            
        #servo1 (elbow) open an amout
        t_end = time() + 0.5 
        while time() > t_end:
            self.arm.serv1_turn_left() #serv1_turn_right()
            sleep(0.001)

        #Servo0 (base) down an amount
        t_end = time() + 0.5 
        while time() > t_end:
            self.arm.serv0_turn_left() #serv0_turn_left()
            sleep(0.001)

        #servo5 (claw) open
        t_end = time() + 0.5
        while time() > t_end:
            self.arm.open_claw()
            sleep(0.001)
            
        print("Servo script done")
        
        
        
        print("Beginning driving")

        #Turn towards center
        t_end = time() + 0.5
        while time() > t_end:
            self.drive.move_right()
        self.drive.move_stop()
        
        #drive forward for X
        t_end = time() + 0.5
        while time() > t_end:
            self.drive.move_forward()
        self.drive.move_stop()
        
        #turn towards other side through tunnel
        t_end = time() + 0.5
        while time() > t_end:
            self.drive.move_left()
        self.drive.move_stop()
        
        #go straight until other side
        t_end = time() + 0.5
        while time() > t_end:
            self.drive.move_straight()
        self.drive.move_stop()
        
        #deploy arm if needed