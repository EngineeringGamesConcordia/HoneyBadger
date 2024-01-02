from pyPS4Controller.controller import Controller
from arm import Arm
from drive import Drive
from relay import Relay
from automation import Automation
from motors import dcMotor
import time

'''
------------------------------ CONTROLLER CHEAT SHEET ------------------------------
    share               start manual control
    options             start automation
    arrows              drive (front, back, left, right)
    right joystick      arm (x-pos, x-neg, y-pos, y-neg)
    circle              start throw
    square              start vacuum
    x                   stop vacuum
    triangle            stop throw
    R1                  stepper servo cw
    L1                  stepper servo ccw
    R2                  gas    
'''

class HoneyController(Controller):

    manualDeadZone = 10000
    armdeadzone = 2000
#    drivedeadzone = 3000
    
    def __init__(self, arm, drivesys, relay, automation, **kwargs):
        self.arm = arm
        self.drive = drivesys
        self.relay = relay
        self.automation = automation
        
        self.lastValueArmX = 0
        self.lastValueArmNegX = 0
        self.lastValueArmY = 0
        self.lastValueArmNegY =0
#        self.lastValueDriveX = 0
#        self.lastValueDriveNegX =0
#        self.lastValueDriveY = 0
#        self.lastValueDriveNegY=0
        
        self.lastValueStepperL1 = False
        self.lastValueStepperR1 = False
        
        self.gas =0
        
        self.dPadL = False
        self.dPadR = False
        self.dPadU = False
        self.dPadD = False

        Controller.__init__(self, **kwargs)
        self.state = False #IKFunctions Drive
        #on true: indivual joint control

    '''
    ------------------------------ START AUTOMATIC CONTROL ------------------------------
    '''
    def on_options_press(self):
        print("start automatic control")
        self.drive.start_automatic_control()

    '''
    ------------------------------ START MANUAL CONTROL ------------------------------
    '''
    def on_share_press(self):
        self.state =not(self.state)        
        print("start manual control" + str(self.state))
        self.gas =0
        self.lastValueArmX = 0
        self.lastValueArmNegX = 0
        self.lastValueArmY = 0
        self.lastValueArmNegY =0

    '''
    ------------------------------ DRIVE SYSTEM ------------------------------
    '''
    def on_R2_press(self, value):
        value= (value+2**15)/(2**16)
        self.gas = value
        print("Gas Value" + str(self.gas))
        
    def on_R2_release(self):
        self.gas = 0
    
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
    ------------------------------ ARM SYSTEM ------------------------------
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
    ------------------------------ ARM SYSTEM - Stepper ------------------------------
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
        print("start sucking")
        self.relay.start_vacuum()

    # Stop vacuum
    def on_x_press(self):
        print("stop vacuum")
        self.relay.stop_vacuum()

    '''
    ------------------------------ THROW SYSTEM ------------------------------
    '''
    # Start throw
    def on_circle_press(self):
        print("start sucking")
        self.relay.start_throw()

    # Stop throw
    def on_triangle_press(self):
        print("stop vacuum")
        self.relay.stop_throw()
        
    '''
    ------------------------------TICK SYSTEM ------------------------------
    '''   
    def checker(self):      

        if(self.state):
            #Servo 0 Turn Left
            if(self.lastValueArmY> self.manualDeadZone):
                self.arm.serv0_turn_left()
            #Servo 0 Turn Right    
            if(self.lastValueArmNegY <-self.manualDeadZone):
                self.arm.serv0_turn_right()           
            #Servo 1 Turn Right
            if(self.lastValueArmX >self.manualDeadZone):
                self.arm.serv1_turn_right()   
            #Servo 1 Turn Left
            if(self.lastValueArmNegX <-self.manualDeadZone):
                self.arm.serv1_turn_left()        
        else:
            #Arm
            if(self.lastValueArmY > self.armdeadzone):
                self.arm.y_pos(self.lastValueArmY)  
                
            if(self.lastValueArmNegY < -self.armdeadzone):
                self.arm.y_neg(self.lastValueArmNegY)             

            if(self.lastValueArmX >self.armdeadzone): 
                self.arm.x_pos(self.lastValueArmX)
            
            if(self.lastValueArmNegX < -self.armdeadzone):
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
            
        #Stepper Servo
        if(self.lastValueStepperL1):
            self.arm.stepper_turn_left() 
                
        if(self.lastValueStepperR1):
            self.arm.stepper_turn_right()  

