from pyPS4Controller.controller import Controller
from arm import Arm
from drive import Drive
from suck import Suck

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
    square              start suck
    x                   stop suck
'''

class BadgerController(Controller):
    def __init__(self, drive, arm, suck, interface, ds4drv):
        self.arm = arm
        self.drive = drive
        self.suck = suck

        Controller.__init__(self, interface, ds4drv)

    '''
    ------------------------------ START AUTOMATIC CONTROL ------------------------------
    '''
    def on_options_press(self):
        print("start automatic control")
        # self.drive.start_automatic_control()

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
        self.arm.x_pos()

    # Arm x-neg
    def on_R3_down(self, value):
        print("arm x-neg")
        self.arm.x_neg()

    # Arm y-pos
    def on_R3_left(self, value):
        print("arm y-pos")
        self.arm.y_pos()

    # Arm y-neg
    def on_R3_right(self, value):
        print("arm y-neg")
        self.arm.y_neg()

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
    ------------------------------ SUCK SYSTEM ------------------------------
    '''
    # Start sucking
    def on_square_press(self):
        print("start sucking")
        self.suck.start_suck()

    # Stop sucking
    def on_x_press(self):
        print("stop sucking")
        self.suck.stop_suck()