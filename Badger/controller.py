from nntplib import decode_header
from pyPS4Controller.controller import Controller
from arm import Arm
from drive import Drive
from vacuum import Vacuum
from automation import Automation
from motors import dcMotor
from motors import stepperMotor
import time

'''
------------------------------ CONTROLLER CHEAT SHEET ------------------------------
    share               start automatic control
    options             start manual control
    left joystick       drive (front, back, left, right)
    right joystick      arm (x-pos, x-neg, y-pos, y-neg)
    square              start vacuum
    x                   stop vacuum
    L2                  open claw
    R2                  close claw
    L1                  turn claw wrist left
    R1                  turn claw wrist right
'''

class BadgerController(Controller):
    clawDeadZone = 10000
    deadzone = 2000

    def __init__(self, arm, claw, drive, vacuum, wrist, automation, **kwargs):
        self.arm = arm
        self.claw = claw
        self.drive = drive
        self.vacuum = vacuum
        self.wrist = wrist
        self.automation = automation
        
        self.lastValueArmX = 0
        self.lastValueArmNegX = 0
        self.lastValueArmY = 0
        self.lastValueArmNegY =0
        
        
        self.lastValueDriveX = 0
        self.lastValueDriveNegX =0
        self.lastValueDriveY = 0
        self.lastValueDriveNegY=0
        
        self.lastValueOpenClaw = 0
        self.lastValueCloseClaw = 0
        
        
        
        Controller.__init__(self, **kwargs)



    '''
    ------------------------------ START AUTOMATIC CONTROL ------------------------------
    '''
    def on_options_press(self):
        print("start automatic control")
        self.automation.start()

    '''
    ------------------------------ START MANUAL CONTROL ------------------------------
    '''
    def on_share_press(self):
        print("start manual control")
        # self.drive.start_manual_control()

    '''
    ------------------------------ DRIVE SYSTEM ------------------------------
    '''
    # Drive front
    def on_up_arrow_press(self):
        self.drive.move_front()
        print("moved front")
        
    #Stop X
    def on_up_down_arrow_release(self):
        self.drive.move_stop()
        print("i stopped X")
        
    # Drive back
    def on_down_arrow_press(self):
        self.drive.move_back()
        print("moved back")
        
    # Drive left
    def on_left_arrow_press(self):
        self.drive.move_left()
        print("moved left")
        

    # Drive right
    def on_right_arrow_press(self):
        self.drive.move_right()
        print("moved right")
    #Stopped Y
    def on_left_right_arrow_release(self):
        self.drive.move_stop()
        print("i stopped Y")

    '''
    ------------------------------ ARM SYSTEM - x and y axis ------------------------------
    '''
    # Arm x-pos
    def on_R3_up(self, value):
        self.lastValueArmX = value;
        print("arm x-pos")
       
    # Arm x-neg
    def on_R3_down(self, value):
        self.lastValueArmNegX = value;
        print("arm x-neg")
        
    def on_R3_x_at_rest(self):
        self.lastValueArmX = 0
        self.lastValueArmNegX = 0
        
    # Arm y-pos
    def on_R3_left(self, value):
        self.lastValueArmY = value;
        print("arm y-pos")

    # Arm y-neg
    def on_R3_right(self, value):
        self.lastValueArmNegY = value;
        print("arm y-neg")
        
    def on_R3_y_at_rest(self):
        self.lastValueArmY = 0
        self.lastValueArmNegY = 0
    '''
    ------------------------------ ARM SYSTEM - Stepper ------------------------------
    '''

    # Turn Right
    def on_R1_press(self):
        print("Stepper Moving Right")
        #insert stepper code for right

    # Turn Left
    def on_L1_press(self):
        print("Stepper Moving Left")
        #insert stepper code for left
    
    '''
    ------------------------------ VACUUM SYSTEM ------------------------------
    '''
    # Start vacuum
    def on_square_press(self):
        print("start vacuum")
        self.vacuum.start_vacuum()
    # Stop vacuum
    def on_x_press(self):
        print("stop vacuum")
        self.vacuum.stop_vacuum()

    '''
    ------------------------------ CLAW SYSTEM ------------------------------
    '''
    # Open claw
    def on_L2_press(self, value):
        value= (value+2**15)
        self.lastValueOpenClaw = value
        
    def on_L2_release(self):
        self.lastValueOpenClaw = 0     
    
    # Close claw
    def on_R2_press(self, value):
        value= (value+2**15)
        self.lastValueCloseClaw = value
    
    def on_R2_release(self):
        self.lastValueCloseClaw = 0

    '''
    ------------------------------ WRIST L+R SYSTEM ------------------------------
    '''
    '''
    # Wrist Turn Left
    def on_left_arrow_press(self):
        print("wrist left")
        self.arm.turn_left()

    # Wrist Turn Right
    def on_right_arrow_press(self):
        print("wrist right")
        self.arm.turn_right()
    '''    
    '''
    ------------------------------ WRIST U+D SYSTEM ------------------------------
    '''
    '''
    # Wrist Go Up
    def on_up_arrow_press(self):
        print("wrist up")
        self.arm.go_up()

    # Wrist Go Down
    def on_down_arrow_press(self):
        print("wrist down")
        self.arm.go_down()
        
    #getting the values of the placeholder    
    '''
    '''
    ------------------------------TICK SYSTEM ------------------------------
    '''   
    def checker(self):      
        #arms if
        if(self.lastValueArmX >0): 
            self.arm.x_pos(self.lastValueArmX)
                
        if(self.lastValueArmNegX < -self.deadzone):
            self.arm.x_neg(self.lastValueArmNegX)
                
        if(self.lastValueArmY >self.deadzone):
            self.arm.y_pos(self.lastValueArmY)  
                
        if(self.lastValueArmNegY <-self.deadzone):
            self.arm.y_neg(self.lastValueArmNegY)            

        #claw if
        if(self.lastValueOpenClaw >self.clawDeadZone):  
            self.arm.open_claw(self.lastValueOpenClaw)
        else:  
            self.lastValueOpenClaw = 0
            #do the same for the close
            
        if(self.lastValueCloseClaw >self.clawDeadZone):    
            self.arm.close_claw(self.lastValueCloseClaw)
        else:
            self.lastValueCloseClaw=0
    
        
