from nntplib import decode_header
from pyPS4Controller.controller import Controller
from arm import Arm
from drive import Drive
from vacuum import Vacuum
from automation import Automation
from motors import dcMotor
import time

'''
------------------------------ CONTROLLER CHEAT SHEET ------------------------------
    share               start manual control
    options             start automatic control
    left joystick       wrist (left,right,up,down)
    right joystick      arm (x-pos, x-neg, y-pos, y-neg), IK
    square              start vacuum
    x                   stop vacuum
    L2                  open claw
    R2                  close claw
    L1                  stepper servo left
    R1                  stepper servo right
    Arrows              Drive (front, back, left, right)
'''

class BadgerController(Controller):
    clawDeadZone = 10000
    deadzone = 2000
    wristdeadzone = 31500

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
#        self.lastValueDriveX = 0
#        self.lastValueDriveNegX =0
#        self.lastValueDriveY = 0
#        self.lastValueDriveNegY=0
        self.lastValueOpenClaw = 0
        self.lastValueCloseClaw = 0
        
        self.lastValueWristDown = 0
        self.lastValueWristUp = 0
        self.lastValueWristLeft = 0
        self.lastValueWristRight = 0
        
        self.lastValueStepperL1 = False
        self.lastValueStepperR1 = False
           
        self.gas =0
        
        self.dPadL = False
        self.dPadR = False
        self.dPadU = False
        self.dPadD = False
        self.beep = True
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
        self.dPadD = True
        print("moved front")
        
    #Stop 
    def on_up_down_arrow_release(self):
        self.dPadU = False
        self.dPadD = False
        print("i stopped X")
        
    # Drive back
    def on_down_arrow_press(self):
        self.dPadU = True
        print("moved back")
        
    # Drive left
    def on_left_arrow_press(self):
        self.dPadR = True
        print("moved left")
        

    # Drive right
    def on_right_arrow_press(self):
        self.dPadL = True
        print("moved right")
    #Stopped 
    def on_left_right_arrow_release(self):
        self.dPadR = False
        self.dPadL = False
        print("i stopped Y")
    '''
    ------------------------------ ARM SYSTEM - x and y axis ------------------------------
    '''
    # Arm x-pos
    def on_R3_right(self, value):
        self.lastValueArmX = value;
       
    # Arm x-neg
    def on_R3_left(self, value):
        self.lastValueArmNegX = value;
        
    def on_R3_x_at_rest(self):
        self.lastValueArmX = 0
        self.lastValueArmNegX = 0
        
    # Arm y-neg
    def on_R3_down(self, value):
        self.lastValueArmY = value;

    # Arm y-pos
    def on_R3_up(self, value):
        self.lastValueArmNegY = value;
        
    def on_R3_y_at_rest(self):
        self.lastValueArmY = 0
        self.lastValueArmNegY = 0
    '''
    ------------------------------ ARM SYSTEM - Stepper Servo ------------------------------
    '''
     
    # Turn Right
    def on_R1_press(self):
        self.lastValueStepperR1 = True
        print("Stepper Moving Right")

    def on_R1_release(self):
        self.lastValueStepperR1 = False
        print("STOP Stepper")
        
    # Turn Left
    def on_L1_press(self):
        self.lastValueStepperL1 = True  
        print("Stepper Moving Left")
        
    def on_L1_release(self):
        self.lastValueStepperL1 = False
        print("STOP Stepper")
    
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
    ------------------------------ START AUTOMATIC CONTROL ------------------------------
    '''
    def on_options_press(self):
        if(self.beep):
            print("start automatic control")
            self.automation.start()
            self.beep= not self.beep           
        
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
        if(not self.beep):  
            if(self.state):
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
                #halfspeed driving    
                if(self.dPadU):
                    self.gas = 0.5
                    self.drive.move_front(self.gas)
                if(self.dPadD):
                    self.gas = 0.5
                    self.drive.move_back(self.gas)    
                if(self.dPadL):
                    self.gas = 0.5
                    self.drive.move_left(self.gas)
                if(self.dPadR):
                    self.gas = 0.5  
                    self.drive.move_right(self.gas)                 
            else:
                #Arm
                if(self.lastValueArmY > self.deadzone):
                    self.arm.y_pos(self.lastValueArmY)  
                    
                if(self.lastValueArmNegY < -self.deadzone):
                    self.arm.y_neg(self.lastValueArmNegY)   
                    
                if(self.lastValueArmX >self.deadzone): 
                    self.arm.x_pos(self.lastValueArmX)
                
                if(self.lastValueArmNegX < -self.deadzone):
                    self.arm.x_neg(self.lastValueArmNegX)   
                #Driving            
                if(self.dPadU):
                    self.drive.move_front(self.gas)
                if(self.dPadD):
                    self.drive.move_back(self.gas)    
                if(self.dPadL):
                    self.drive.move_left(self.gas)
                if(self.dPadR):
                    self.drive.move_right(self.gas) 
            if(self.dPadU==False and self.dPadD==False and self.dPadL==False and self.dPadR==False):
                self.drive.move_stop()                        
            #Wrists   
            if(self.lastValueWristDown >self.wristdeadzone):
                self.arm.go_down()  
                    
            if(self.lastValueWristUp < -self.wristdeadzone):
                self.arm.go_up()  
                
            if(self.lastValueWristLeft < -self.wristdeadzone): 
                self.arm.turn_left()
                    
            if(self.lastValueWristRight > self.wristdeadzone):
                self.arm.turn_right()  
                
            #Stepper Servo
            if(self.lastValueStepperL1):
                self.arm.stepper_turn_left() 
                    
            if(self.lastValueStepperR1):
                self.arm.stepper_turn_right()  
