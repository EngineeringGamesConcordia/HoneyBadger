from numpy import *
from motors import stepperMotor

# reference: https://github.com/aakieu/3-dof-planar/blob/master/InverseKinematics.py

CONTROLLER_SCALE = 2**15
BIG_SERVO_SCALE = 1/(2**12)
SMALL_SERVO_SCALE = 1/(2**14)
CLAW_SCALE = 1/(2**12)
KINEMATIC_SCALE = 2/(2**15)

moveVal = 1
px = 0
py = 0

# ------------------------------ Get angles
def calculate_inverse_kinematic(px, py):
    # lengths of links in cm
    link_bot = 22
    link_mid = 4.2
    link_top = 22

    phi = 180
    phi = deg2rad(phi)

    # equations for inverse kinematics
    wx = px - link_top * cos(phi)
    wy = py - link_top * sin(phi)

    delta = wx ** 2 + wy ** 2
    c2 = (delta - link_bot ** 2 - link_mid ** 2) / (2 * link_bot * link_mid)
    s2 = sqrt(1 - c2 ** 2)  # elbow down
    theta_2 = arctan2(s2, c2)

    s1 = ((link_bot + link_mid * c2) * wy - link_mid * s2 * wx) / delta
    c1 = ((link_bot + link_mid * c2) * wx + link_mid * s2 * wy) / delta
    theta_1 = arctan2(s1, c1)
    theta_3 = phi - theta_1 - theta_2

    # print('theta_1: ', rad2deg(theta_1))
    # print('theta_2: ', rad2deg(theta_2))
    # print('theta_3: ', rad2deg(theta_3))

    return theta_1, theta_2, theta_3


class Arm:
    def __int__(self, base_stepper, base_servo, elbow_servo, wrist_r_servo, wrist_ud_servo, claw_servo):
        print("Init arm")
        print("base_servo: " + str(base_servo))
        print("elbow_servo: " + str(elbow_servo))
        print("wrist_r_servo: " + str(wrist_r_servo))
        print("wrist_ud_servo: " + str(wrist_ud_servo))
        print("claw_servo: " + str(claw_servo))
        self.base_servo = base_servo
        self.elbow_servo = elbow_servo
        self.wrist_r_servo =  wrist_r_servo
        self.wrist_ud_servo = wrist_ud_servo
        self.claw_servo = claw_servo
        self.SLOW_MODE = False

    # ------------------------------ CLAW MOVEMENTS
    def open_claw(self, val):
        print("> arm claw open")
        val = CLAW_SCALE * ((val + CONTROLLER_SCALE) / (2 * CONTROLLER_SCALE)) ** 3
        self.claw_servo.angle = self.claw_servo.angle + val

    def close_claw(self, val):
        print("> arm claw close")
        val = -CLAW_SCALE * ((val + CONTROLLER_SCALE) / (2 * CONTROLLER_SCALE)) ** 3
        self.claw_servo.angle = self.claw_servo.angle + val

    # ------------------------------ ROTATIONAL MOVEMENTS
    def turn_left(self):
        print("> wrist rotating left")
        self.wrist_r_servo.angle = self.wrist_r_servo.angle + moveVal

    def turn_right(self):
        print("> wrist rotating right")
        self.wrist_r_servo.angle = self.wrist_r_servo.angle + moveVal


    # ------------------------------ Move x-pos
    def x_pos(self, val):
        print("> arm x_pos")
        val = KINEMATIC_SCALE * ((val + CONTROLLER_SCALE) / (2 * CONTROLLER_SCALE)) ** 3
        px = px + val;
        theta_1, theta_2, theta_3 = calculate_inverse_kinematic(px, 0)
        self.base_servo.angle = theta_1
        self.elbow_servo.angle = theta_2
        self.wrist_ud_servo.angle = theta_3

    # ------------------------------ Move x-neg
    def x_neg(self, val):
        print("> arm x_neg")
        val = -KINEMATIC_SCALE * ((val + CONTROLLER_SCALE) / (2 * CONTROLLER_SCALE)) ** 3
        px = px + val;
        theta_1, theta_2, theta_3 = calculate_inverse_kinematic(px, 0)
        self.base_servo.angle = theta_1
        self.elbow_servo.angle = theta_2
        self.wrist_ud_servo.angle = theta_3

    # ------------------------------ Move y-pos
    def y_pos(self, val):
        print("> arm y_pos")
        val = KINEMATIC_SCALE * ((val + CONTROLLER_SCALE) / (2 * CONTROLLER_SCALE)) ** 3
        py = py + val;
        theta_1, theta_2, theta_3 = calculate_inverse_kinematic(0, py)
        self.base_servo.angle = theta_1
        self.elbow_servo.angle = theta_2
        self.wrist_ud_servo.angle = theta_3

    # ------------------------------ Move y-neg
    def y_neg(self, val):
        print("> arm y_neg")
        val = -KINEMATIC_SCALE * ((val + CONTROLLER_SCALE) / (2 * CONTROLLER_SCALE)) ** 3
        py = py + val;
        theta_1, theta_2, theta_3 = calculate_inverse_kinematic(0, py)
        self.base_servo.angle = theta_1
        self.elbow_servo.angle = theta_2
        self.wrist_ud_servo.angle = theta_3

    # ------------------------------ STEPPER Movements
    # Insert stepper codes lol
    
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