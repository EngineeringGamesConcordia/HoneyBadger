from pyPS4Controller.controller import Controller
from arm import Arm
from claw import Claw
from drive import Drive
from vacuum import Vacuum
from automation import Automation

'''
------------------------------ CONTROLLER CHEAT SHEET ------------------------------
    share               start automatic control
    options             start manual control
    left joystick       drive (front, back, left, right)
    right joystick      arm (x-pos, x-neg, y-pos, y-neg)
    down arrow          height 1 (lowest)
    left arrow          height 2 (middle)
    up arrow            height 3 (highest)
    circle              height to reach ball on floor
    square              start vacuum
    x                   stop vacuum
    L1                  open claw
    R1                  close claw
    L2                  turn claw wrist left
    R2                  turn claw wrist right
'''

class BadgerController(Controller):
    def __init__(self, arm, claw, drive, vacuum, wrist, automation, interface, ds4drv):
        self.arm = arm
        self.claw = claw
        self.drive = drive
        self.vacuum = vacuum
        self.wrist = wrist
        self.automation = automation

        Controller.__init__(self, interface, ds4drv)

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
    def on_L3_up(self, value):
        print("move front")
        self.drive.move_front()

    # Drive back
    def on_L3_down(self, value):
        print("move back")
        self.drive.move_back()

    # Drive left
    def on_L3_left(self, value):
        print("move left")
        self.drive.move_left()

    # Drive right
    def on_L3_right(self, value):
        print("move right")
        self.drive.move_right()

    '''
    ------------------------------ ARM SYSTEM - x and y axis ------------------------------
    '''
    # Arm x-pos
    def on_R3_up(self, value):
        print("arm x-pos")
        self.arm.x_pos(value)

    # Arm x-neg
    def on_R3_down(self, value):
        print("arm x-neg")
        self.arm.x_neg(value)

    # Arm y-pos
    def on_R3_left(self, value):
        print("arm y-pos")
        self.arm.y_pos(value)

    # Arm y-neg
    def on_R3_right(self, value):
        print("arm y-neg")
        self.arm.y_neg(value)

    '''
    ------------------------------ ARM SYSTEM - z axis ------------------------------
    '''
    # Height floor - reach ball
    def on_circle_press(self):
        print("arm floor")
        self.arm.height_floor()

    # Height 1 - lowest
    def on_down_arrow_press(self):
        print("arm height 1")
        self.arm.height_1()

    # Height 2 - middle
    def on_left_arrow_press(self):
        print("arm height 2")
        self.arm.height_2()

    # Height 3 - highest
    def on_up_arrow_press(self):
        print("arm height 3")
        self.arm.height_3()
    
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
    def on_L1_press(self):
        print("claw open")
        self.claw.open_claw()
    
    # Close claw
    def on_R1_press(self):
        print("claw close")
        self.claw.close_claw()

    '''
    ------------------------------ WRIST SYSTEM ------------------------------
    '''

    # Open claw
    def on_L2_press(self):
        print("wrist left")
        self.wrist.turn_left()

    # Close claw
    def on_R2_press(self):
        print("wrist right")
        self.wrist.turn_right()