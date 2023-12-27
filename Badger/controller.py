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


    def __init__(self, arm, claw, drive, vacuum, wrist, automation,lastValueArmX,lastValueArmY,lastValueDriveX, lastValueDriveY,lastValueOpenClaw,lastValueCloseClaw, **kwargs):
        self.arm = arm
        self.claw = claw
        self.drive = drive
        self.vacuum = vacuum
        self.wrist = wrist
        self.automation = automation
        self.lastValueArmX = lastValueArmX
        self.lastValueArmY =lastValueArmY
        self.lastValueDriveX = lastValueDriveX
        self.lastValueDriveY = lastValueDriveY
        self.lastValueOpenClaw = lastValueOpenClaw
        self.lastValueCloseClaw = lastValueCloseClaw
        
        
        Controller.__init__(self, **kwargs)



    '''
    ------------------------------ START AUTOMATIC CONTROL ------------------------------
    '''
    lastValueArmX = 0 
    lastValueArmY = 0
    lastValueDriveX = 0
    lastValueDriveY = 0
    lastValueOpenClaw = 0
    lastValueCloseClaw = 0
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
    def on_L3_up(self, value):
        self.lastValueDriveY = value
        print("move front")
        self.drive.move_front()

    # Drive back
    def on_L3_down(self, value):
        self.lastValueDriveY = value
        print("move back")
        self.drive.move_back()

    # Drive left
    def on_L3_left(self, value):
        self.lastValueDriveX = value
        print("move left")
        self.drive.move_left()

    # Drive right
    def on_L3_right(self, value):
        self.lastValueDriveX = value
        print("move right")
        self.drive.move_right()

    '''
    ------------------------------ ARM SYSTEM - x and y axis ------------------------------
    '''
    # Arm x-pos
    def on_R3_up(self, value):
        self.lastValueArmX = value;
        print("arm x-pos")
        self.arm.x_pos(value)

    # Arm x-neg
    def on_R3_down(self, value):
        self.lastValueArmX = value;
        print("arm x-neg")
        self.arm.x_neg(value)

    # Arm y-pos
    def on_R3_left(self, value):
        self.lastValueArmY = value;
        print("arm y-pos")
        self.arm.y_pos(value)

    # Arm y-neg
    def on_R3_right(self, value):
        self.lastValueArmY = value;
        print("arm y-neg")
        self.arm.y_neg(value)

    '''
    ------------------------------ ARM SYSTEM - Stepper ------------------------------
    '''

    # Turn Right
    def on_right_arrow_press(self):
        print("Stepper Moving Right")
        #insert stepper code for right

    # Turn Left
    def on_left_arrow_press(self):
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
        lastValueOpenClaw = value
        print("claw open")
        self.arm.open_claw(value)
    
    # Close claw
    def on_R2_press(self, value):
        lastValueCloseClaw = value
        print("claw close")
        self.arm.close_claw(value)

    '''
    ------------------------------ WRIST SYSTEM ------------------------------
    '''

    # Wrist Turn Left
    def on_L1_press(self):
        print("wrist left")
        self.arm.turn_left()

    # Wrist Turn Right
    def on_R1_press(self):
        print("wrist right")
        self.arm.turn_right()
        
    #getting the values of the placeholder    

    def checker(self):
            print("WompWomp value of arm X: " + str(self.lastValueArmX))
            print("WompWomp value of arm Y: " + str(self.lastValueArmY))
            print("WompWomp value of drive X: " + str(self.lastValueDriveX))
            print("WompWomp value of drive Y: " + str(self.lastValueDriveY))
            print("WompWomp value of claw open: " + str(self.lastValueOpenClaw))
            print("WompWomp value of claw close: " + str(self. lastValueCloseClaw))
    
        