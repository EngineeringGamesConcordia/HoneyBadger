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
    left joystick       drive (front, back, left, right)
    right joystick      arm (x-pos, x-neg, y-pos, y-neg)
    circle              start throw
    square              start vacuum
    x                   stop vacuum
    triangle            stop throw
    R1                  stepper servo cw
    L1                  stepper servo ccw
    
'''

class HoneyController(Controller):

    manualDeadZone = 10000
    armdeadzone = 2000
    drivedeadzone = 3000
    
    def __init__(self, arm, drivesys, relay, automation, **kwargs):
        self.arm = arm
        self.drive = drivesys
        self.relay = relay
        self.automation = automation
        
        self.lastValueArmX = 0
        self.lastValueArmNegX = 0
        self.lastValueArmY = 0
        self.lastValueArmNegY =0
        self.lastValueDriveX = 0
        self.lastValueDriveNegX =0
        self.lastValueDriveY = 0
        self.lastValueDriveNegY=0
        
        self.lastValueStepperL1 = False
        self.lastValueStepperR1 = False
        
        self.dPadL = False
        self.dPadR = False

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
        self.lastValueArmX = 0
        self.lastValueArmNegX = 0
        self.lastValueArmY = 0
        self.lastValueArmNegY =0

    '''
    ------------------------------ DRIVE SYSTEM ------------------------------
    '''
    
    # Go right
    def on_L3_right(self, value):
        self.lastValueDriveX = value;
        print("drive x-pos")
        
    # Go left
    def on_L3_left(self, value):
        self.lastValueDriveNegX = value;
        print("drive x-neg")
        
    def on_L3_x_at_rest(self):
        self.lastValueDriveX = 0
        self.lastValueDriveNegX = 0
        
    # Go backward
    def on_L3_down(self, value):
        self.lastValueDriveY = value;
        print("drive y-neg")

    # Go forward
    def on_L3_up(self, value):
        self.lastValueDriveNegY = value;
        print("drive y-pos")
        
    def on_L3_y_at_rest(self):
        self.lastValueDriveY = 0
        self.lastValueDriveNegY = 0
        
    # Turn left
    def on_left_arrow_press(self):
        self.dPadL = True
        print("moved left")
        
    # Turn right
    def on_right_arrow_press(self):
        self.dPadR = True
        print("moved right")
            
    #Stopped 
    def on_left_right_arrow_release(self):
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
        if(self.lastValueDriveY > self.drivedeadzone):
            print ("Y = " + str(self.lastValueDriveY))
            self.drive.move_back(-self.lastValueDriveY)  
            
        if(self.lastValueDriveNegY < -self.drivedeadzone):
            print ("Y_neg = " + str(self.lastValueDriveNegY))
            self.drive.move_front(self.lastValueDriveNegY)             

        if(self.lastValueDriveX >self.drivedeadzone): 
            print ("X = " + str(self.lastValueDriveX))
            self.drive.move_right(self.lastValueDriveX)
            
        if(self.lastValueDriveNegX < -self.drivedeadzone):
            print ("X_neg = " + str(self.lastValueDriveNegX))
            self.drive.move_left(-self.lastValueDriveNegX)
            
        if(self.dPadL==False and self.dPadR==False and self.lastValueDriveY == 0 and self.lastValueDriveNegY == 0 and self.lastValueDriveX == 0 and self.lastValueDriveNegX == 0):
            self.drive.stop()
            
        if(self.dPadL):
            self.drive.turn_left()
            
        if(self.dPadR):
            self.drive.turn_right() 
            
        #Stepper Servo
        if(self.lastValueStepperL1):
            self.arm.stepper_turn_left() 
                
        if(self.lastValueStepperR1):
            self.arm.stepper_turn_right()  

