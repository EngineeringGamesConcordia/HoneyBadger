from pyPS4Controller.controller import Controller
from arm import Arm
from drive import Drive
from throw import Throw
from vacuum import Vacuum

'''
------------------------------ CONTROLLER CHEAT SHEET ------------------------------
    share               start automation
    options             start manual control
    left joystick       drive (front, back, left, right)
    right joystick      arm (x-pos, x-neg, y-pos, y-neg)
    circle              height to reach ball on floor
    square              start vacuum
    x                   stop vacuum
    triangle            place ball automatically in tube
'''

class HoneyController(Controller):
    def __init__(self, drive, arm, throw, vacuum, automation, interface, ds4drv):
        self.arm = arm
        self.drive = drive
        self.throw = throw
        self.vacuum = vacuum
        self.automation = automation

        Controller.__init__(self, interface, ds4drv)

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
        print("start manual control")
        self.drive.start_manual_control()

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
    ------------------------------ ARM SYSTEM ------------------------------
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

    # Height floor - reach ball
    def on_circle_press(self):
        print("arm floor")
        self.arm.height_floor()

    '''
    ------------------------------ VACUUM SYSTEM ------------------------------
    '''
    # Start vacuum
    def on_square_press(self):
        print("start sucking")
        self.vacuum.start_vacuum()

    # Stop vacuum
    def on_x_press(self):
        print("stop vacuum")
        self.arm.stop_vacuum()

    '''
    ------------------------------ THROW SYSTEM ------------------------------
    '''
    # Place ball
    def on_triangle_press(self):
        print("place ball")
        self.arm.place_ball()
