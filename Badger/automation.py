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
 
        
        print("Beginning driving")

        #Turn towards center and move forward
        t_end = time() + 0.75
        while time() < t_end:
            self.drive.move_right(1)
        self.drive.move_stop()
        
        #drive forward for X
#        t_end = time() + 1
#        while time() < t_end:
#            self.drive.move_front(1)
#        self.drive.move_stop()
        

        #Suck on my balls bitches
        """
        t_end = time() + 25
        while time() <t_end:
           
        """
            #Bring arm down to ball height
            #Swing a bit
            
            
            
            #Turn to rocks
            #drop ball
            

            #drop ball
        print("Automation Ended")
        