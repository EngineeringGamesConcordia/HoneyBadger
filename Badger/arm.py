from numpy import *
import tinyik
from motors import stepperMotor
import RPi.GPIO as GPIO
from time import sleep
# reference: https://github.com/aakieu/3-dof-planar/blob/master/InverseKinematics.py

CONTROLLER_SCALE = 2**15
BIG_SERVO_SCALE = 1/(2**18)
SMALL_SERVO_SCALE = 1/(2**18)
CLAW_SCALE = 1/(2**18)
KINEMATIC_SCALE = 2/(2**18)

moveVal = 2
px = 22
py = 22

# ------------------------------ Get angles
def calculate_inverse_kinematic(px, py):

    lengths of the arm are 22
    arm = tinyik.Actuator(['z', [22., 0., 0.], 'z', [22., 0., 0.]])
    theta_1 = 0
    theta_2 = 0

    ikangles = [theta_1, theta_2]
    arm.ee = [px, py]
    ikangles = round(rad2deg(arm.angles))
    
    return theta_1, theta_2


class Arm:
    global px
    global py
    global moveVal
    
    def __init__(self, base_stepper, kit, angles):
        global px
        global py
        global moveVal
        print("Init arm")
        self.base_servo = angles[0]
        self.elbow_servo = angles[1]
        self.wrist_r_servo =  angles[2]
        self.wrist_ud_servo = angles[3]
        self.claw_servo = angles[4]
        self.kit = kit
        self.kit.servo[0].angle = angles[0]
        self.kit.servo[1].angle = angles[1]
        self.kit.servo[2].angle = angles[2]
        self.kit.servo[3].angle = angles[3]
        self.kit.servo[4].angle = angles[4]
        self.px = px
        self.py = py
        self.moveVal = moveVal
        self.SLOW_MODE = False

    # ------------------------------ CLAW MOVEMENTS
    def open_claw(self, val):
        val = CLAW_SCALE * ((((val + CONTROLLER_SCALE) / (2 * CONTROLLER_SCALE)) ** 3) + 2**15)
        self.claw_servo = self.claw_servo + val
        self.kit.servo[4].angle = self.claw_servo

    def close_claw(self, val):
        val = CLAW_SCALE * ((((val + CONTROLLER_SCALE) / (2 * CONTROLLER_SCALE)) ** 3) + 2**15)
        self.claw_servo = self.claw_servo - val
        self.kit.servo[4].angle = self.claw_servo

    # ------------------------------ ROTATIONAL MOVEMENTS
    def turn_left(self):
        print("> wrist rotating left")
        self.wrist_r_servo = self.wrist_r_servo - self.moveVal
        self.kit.servo[2].angle = self.wrist_r_servo

    def turn_right(self):
        print("> wrist rotating right")
        self.wrist_r_servo = self.wrist_r_servo + self.moveVal
        self.kit.servo[2].angle = self.wrist_r_servo

    # ------------------------------ ROTATIONAL MOVEMENTS
    def go_up(self):
        print("> wrist up")
        self.wrist_ud_servo = self.wrist_ud_servo - self.moveVal
        self.kit.servo[3].angle = self.wrist_ud_servo

    def go_down(self):
        print("> wrist down")
        self.wrist_ud_servo = self.wrist_ud_servo + self.moveVal
        self.kit.servo[3].angle = self.wrist_ud_servo

    # ------------------------------ Move x-pos
    def x_pos(self, val):
        print("> arm22 x_pos")
        val = KINEMATIC_SCALE * ((((val + CONTROLLER_SCALE) / (2 * CONTROLLER_SCALE)) ** 3) + 2**15)
        self.px = self.px + val;
        print ("px = " + str(self.px))
        theta_1, theta_2 = calculate_inverse_kinematic(self.px, self.py)
        print ("theta1 theta2 = " + str(theta_1) + "   " + str(theta_2))
        self.kit.servo[0].angle = theta_1
        self.kit.servo[1].angle = theta_2

    # ------------------------------ Move x-neg
    def x_neg(self, val):
        print("> arm22 x_neg")
        val = KINEMATIC_SCALE * ((((val + CONTROLLER_SCALE) / (2 * CONTROLLER_SCALE)) ** 3) + 2**15)
        self.px = self.px - val;
        print ("px = " + str(self.px))
        theta_1, theta_2 = calculate_inverse_kinematic(self.px, self.py)
        print ("theta1 theta2 = " + str(theta_1) + "   " + str(theta_2))
        self.kit.servo[0].angle = theta_1
        self.kit.servo[1].angle = theta_2

    # ------------------------------ Move y-pos
    def y_pos(self, val):
        print("> arm22 y_pos")
        val = KINEMATIC_SCALE * ((((val + CONTROLLER_SCALE) / (2 * CONTROLLER_SCALE)) ** 3) + 2**15)
        self.py = self.py - val;
        print ("py = " + str(self.py))
        theta_1, theta_2 = calculate_inverse_kinematic(self.px, self.py)
        print ("theta1 theta2 = " + str(theta_1) + "   " + str(theta_2))
        self.kit.servo[0].angle = theta_1
        self.kit.servo[1].angle = theta_2

    # ------------------------------ Move y-neg
    def y_neg(self, val):
        print("> arm22 y_neg")
        val = KINEMATIC_SCALE * ((((val + CONTROLLER_SCALE) / (2 * CONTROLLER_SCALE)) ** 3) + 2**15)
        self.py = self.py + val;
        print ("py = " + str(self.py))
        theta_1, theta_2 = calculate_inverse_kinematic(self.px, self.py)
        print ("theta1 theta2 = " + str(theta_1) + "   " + str(theta_2))
        self.kit.servo[0].angle = theta_1
        self.kit.servo[1].angle = theta_2

    # ------------------------------ STEPPER Set up

    # Insert stepper codes lol
    def cw_stepper(self):
        GPIO.output(DIR, CW)
        #going forward
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
    def ccw_stepper(self):
        GPIO.output(DIR, CCW)
        GPIO.output(STEP, GPIO.HIGH)
        sleep(delay)
        GPIO.output(STEP, GPIO.LOW)
        sleep(delay)
    
"""
    # ------------------------------ Move down
    def move_down(self):
        print("> arm height floor")
        theta_1, theta_2, theta_3 = calculate_inverse_kinematic(0, 0)  # need to find (x, y) coordinates
        self.base_servo.angle = theta_1
        self.elbow_servo.angle = theta_2
        self.wrist_ud_servo.angle = theta_3

    # ------------------------------ Move up
    def move_up(self):
        print("> arm height 1")
        theta_1, theta_2, theta_3 = calculate_inverse_kinematic(0, 0)  # need to find (x, y) coordinates
        self.base_servo.angle = theta_1
        self.elbow_servo.angle = theta_2
        self.wrist_ud_servo.angle = theta_3
"""