from arm import Arm
from drive import Drive
from vacuum import Vacuum
from motors import dcMotor
from time import sleep, time

class Automation:
    def __init__(self, arm, drive):
        self.arm = arm
        self.drive = drive
        self.flipper = False
        print("Init automation")
        
    def start(self):
        self.flipper = False
        print("> automation start")
        #Badger sets down Honey
        #Servo3 (wrist down an amount
        t_end = time() + 0.5 #5 is second amount the wrist will go up
        while time() > t_end:
            self.arm.go_down() #arm.go_down()
            sleep(0.001)
            
        #servo1 (elbow) open an amout
        t_end = time() + 0.5 
        while time() > t_end:
            self.arm.serv1_turn_left() #serv1_turn_right()
            sleep(0.001)

        #Servo0 (base) up an amount
        t_end = time() + 0.5 
        while time() > t_end:
            self.arm.serv0_turn_right() #serv0_turn_left()
            sleep(0.001)

        #Stepper Servo(base) left an amount
        t_end = time() + 0.5 
        while time() > t_end:
            self.arm.stepper_turn_left() #serv0_turn_left()
            sleep(0.001)
            
        #servo1 (elbow) open an amout and servo0 (base) down an amount
        t_end = time() + 1.0 
        while time() > t_end:
            self.arm.serv1_turn_left() #serv1_turn_right()
            self.arm.serv0_turn_right()
            sleep(0.001)

        #servo1 (elbow) close an amount and wrist go up
        t_end = time() + 0.5 
        while time() > t_end:
            self.arm.serv1_turn_left() #serv1_turn_right()
            self.arm.go_up()
            sleep(0.001)


        #servo5 (claw) open
        t_end = time() + 0.5
        while time() > t_end:
            self.arm.open_claw()
            sleep(0.001)
            
        print("Servo script done")
        
        #Wait for honey to move away
        sleep(5)
        
        print("Beginning driving")

        #Turn towards center and move forward
        t_end = time() + 0.5
        while time() > t_end:
            drive.move_left()
            drive.move_forward()
        drive.move_stop()
        
        #drive forward for X
        t_end = time() + 0.5
        while time() > t_end:
            drive.move_forward()
        drive.move_stop()
        
        #turn towards other side through tunnel
        t_end = time() + 0.5
        while time() > t_end:
            drive.move_left()
        drive.move_stop()
        
        #turn backwards
        t_end = time() + 1.0
        while time() > t_end:
            drive.move_left()
        drive.move_stop()
        
        #fully extend arm (stepper to the middle)
        t_end = time() + 0.5 
        while time() > t_end:
            self.arm.stepper_turn_right() #serv0_turn_left()
            sleep(0.001)
            
        
        #servo1 (elbow) open an amout and servo0 (base) up an amount, until fully extended
        t_end = time() + 2.0 
        while time() > t_end:
            self.arm.serv1_turn_right() #serv1_turn_right()
            self.arm.serv0_turn_right()
            sleep(0.001)
            
        #go straight until other side
        t_end = time() + 1.5
        while time() > t_end:
            drive.move_back()
        drive.move_stop()
        
        #deploy arm if needed