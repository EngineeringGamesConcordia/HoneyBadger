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
    wristdeadzone = 32000

    def __init__(self, arm, drive, vacuum, wrist, automation, **kwargs):
        self.arm = arm
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
        
        self.lastValueWristDown = 0
        self.lastValueWristUp = 0
        self.lastValueWristLeft = 0
        self.lastValueWristRight = 0
        
        self.lastValueBaseDown = 0
        self.lastValueBaseUp = 0
        self.lastValueBaseLeft = 0
        self.lastValueBaseRight = 0
        
        self.lastValueElbowDown = 0
        self.lastValueElbowUp = 0
        self.lastValueElbowLeft = 0
        self.lastValueElbowRight = 0     
        self.gas =0
        
        self.dPadL = False
        self.dPadR = False
        self.dPadU = False
        self.dPadD = False
        Controller.__init__(self, **kwargs)
        self.state = False #IKFunctions Drive and Gas
        #on true: indivual joint control, no drive, open close claw instead of gas
        

    '''
    ------------------------------ STATE CONTROL (CLAW DRIVE GAS JOINTS)------------------------------
    '''
    def on_share_press(self):
        self.state =not(self.state)        
        print("start manual control" + str(self.state))
        self.gas =0
        self.lastValueCloseClaw = 0
        self.lastValueOpenClaw = 0
        self.lastValueArmX = 0
        self.lastValueArmNegX = 0
        self.lastValueArmY = 0
        self.lastValueArmNegY =0
        # self.drive.start_manual_control()
    
      # GAS GAS GAS && CLOSE
    def on_R2_press(self, value):
        if(self.state == False):
            value= (value+2**15)/(2**16)
            self.gas = value
            print("Gas Value" + str(self.gas))
        else:
            value= (value+2**15)
            self.lastValueCloseClaw = value
            print("Close Value" + str(self.lastValueCloseClaw))

    def on_R2_release(self):
        if(self.state == False):
            self.gas = 0
        else:    
            self.lastValueCloseClaw = 0
    
        
    def on_L2_press(self, value):
        if(self.state == True):
            value= (value+2**15)
            self.lastValueOpenClaw = value
            print("Open Value" + str(self.lastValueOpenClaw))
        
    def on_L2_release(self):
        if(self.state == True):
            self.lastValueOpenClaw = 0     





    '''
    ------------------------------ DRIVE SYSTEM ------------------------------
    '''
    # Drive front
    def on_up_arrow_press(self):
        if(self.state == False):
            self.dPadU = True
            print("moved front")
        
    #Stop 
    def on_up_down_arrow_release(self):
        if(self.state == False):
            self.dPadU = False
            self.dPadD = False
            print("i stopped X")
        
    # Drive back
    def on_down_arrow_press(self):
        if(self.state == False):
            self.dPadD = True
            print("moved back")
        
    # Drive left
    def on_left_arrow_press(self):
        if(self.state == False):
            self.dPadL = True
            print("moved left")
        

    # Drive right
    def on_right_arrow_press(self):
        if(self.state == False):
            self.dPadR = True
            print("moved right")
    #Stopped 
    def on_left_right_arrow_release(self):
        if(self.state == False):
            self.dPadR = False
            self.dPadL = False
            print("i stopped Y")
    '''
    ------------------------------ ARM SYSTEM - x and y axis ------------------------------
    '''
    # Arm x-pos
    def on_R3_right(self, value):
        self.lastValueArmX = value;
        if(self.state):
            print("arm x-pos")
        
       
    # Arm x-neg
    def on_R3_left(self, value):
        self.lastValueArmNegX = value;
        if(self.state):
            print("arm x-neg")
        
    def on_R3_x_at_rest(self):
        self.lastValueArmX = 0
        self.lastValueArmNegX = 0
        
    # Arm y-neg
    def on_R3_down(self, value):
        self.lastValueArmY = value;
        if(self.state):
            print("arm y-neg")

    # Arm y-pos
    def on_R3_up(self, value):
        self.lastValueArmNegY = value;
        if(self.state):
            print("arm y-pos")
        
    def on_R3_y_at_rest(self):
        self.lastValueArmY = 0
        self.lastValueArmNegY = 0
    '''
    ------------------------------ ARM SYSTEM - Stepper ------------------------------
    '''

    # Turn Right
    def on_R1_press(self):
        self.arm.cw_stepper()
        print("Stepper Moving Right")
        #insert stepper code for right
    # Turn Left
    def on_L1_press(self):
        self.arm.ccw_stepper()
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


    '''
    ------------------------------ WRIST L+R SYSTEM ------------------------------TO BE FIXED
    '''

    # Wrist Turn Left
    def on_L3_left(self, value):
        self.lastValueWristLeft = value
        self.arm.turn_left()

    # Wrist Turn Right
    def on_L3_right(self, value):
        self.lastValueWristRight = value
        print("wrist right")
        
    def on_L3_x_at_rest(self):
        self.lastValueWristRight = 0
        self.lastValueWristLeft = 0
   
    '''
    ------------------------------ WRIST U+D SYSTEM ------------------------------TO BE FIXED
    '''

    # Wrist Go Up
    def on_L3_up(self, value):
        self.lastValueWristUp = value
        print("wrist up")

    # Wrist Go Down
    def on_L3_down(self, value):
        self.lastValueWristDown = value
        print("wrist down")
        
    def on_L3_y_at_rest(self):
        self.lastValueWristDown = 0
        self.lastValueWristUp = 0
        
    #getting the values of the placeholder    

    '''
    ------------------------------TICK SYSTEM ------------------------------
    '''   
    def checker(self):      

        if(self.state):
            #Servo 0 (Base)
            #Servo 0 Turn Left
            if(self.lastValueArmY> self.clawDeadZone):
                self.arm.serv0_turn_left()
            #Servo 0 Turn Right    
            if(self.lastValueArmNegY <-self.clawDeadZone):
                self.arm.serv0_turn_right()           
            #Servo 1 Turn Right
            if(self.lastValueArmX >self.clawDeadZone):
                self.arm.serv1_turn_right()   
            #Servo 1 Turn Left
            if(self.lastValueArmNegX <-self.clawDeadZone):
                self.arm.serv1_turn_left() 
            
            #Claw
            if(self.lastValueOpenClaw >0):  
                self.arm.open_claw(self.lastValueOpenClaw)
            if(self.lastValueCloseClaw >0):
                self.arm.close_claw(self.lastValueCloseClaw)
        else:
            #Arm
            if(self.lastValueArmY > self.clawDeadZone):
                self.arm.y_pos(self.lastValueArmY)  
                
            if(self.lastValueArmNegY < -self.deadzone):
                self.arm.y_neg(self.lastValueArmNegY)             

            if(self.lastValueArmX >self.clawDeadZone): 
                self.arm.x_pos(self.lastValueArmX)
            
            if(self.lastValueArmNegX < -self.deadzone):
                self.arm.x_neg(self.lastValueArmNegX)   
            #Driving    
            if(self.dPadU==False and self.dPadD==False and self.dPadL==False and self.dPadR==False):
                self.drive.move_stop()                
            if(self.dPadU):
                self.drive.move_front(self.gas)
            if(self.dPadD):
                self.drive.move_back(self.gas)    
            if(self.dPadL):
                self.drive.move_left(self.gas)
            if(self.dPadR):
                self.drive.move_right(self.gas)                    
         #Wrists   
        if(self.lastValueWristDown >self.wristdeadzone):
            self.arm.go_down()  
                
        if(self.lastValueWristUp < -self.wristdeadzone):
            self.arm.go_up()  
            
        if(self.lastValueWristLeft < -self.wristdeadzone): 
            self.arm.turn_left()
                
        if(self.lastValueWristRight > self.wristdeadzone):
            self.arm.turn_right()  
