from motors import servoMotor
from numpy import *

# reference: https://github.com/aakieu/3-dof-planar/blob/master/InverseKinematics.py

# motor pins
BOT = 0
MID = 0
TOP = 0

class Arm:
    def __int__(self):
        print("Init arm")
        self.bot = servoMotor(BOT)
        self.mid = servoMotor(MID)
        self.top = servoMotor(TOP)

    # ------------------------------ Move x-pos
    def x_pos(self, px):
        print("> arm x_pos")
        theta_1, theta_2, theta_3 = self.calculate_inverse_kinematic(px, 0)
        self.bot.set_angle(theta_1)
        self.mid.set_angle(theta_2)
        self.top.set_angle(theta_3)

    # ------------------------------ Move x-neg
    def x_neg(self, px):
        print("> arm x_neg")
        theta_1, theta_2, theta_3 = self.calculate_inverse_kinematic(px, 0)
        self.bot.set_angle(theta_1)
        self.mid.set_angle(theta_2)
        self.top.set_angle(theta_3)

    # ------------------------------ Move y-pos
    def y_pos(self, py):
        print("> arm y_pos")
        theta_1, theta_2, theta_3 = self.calculate_inverse_kinematic(0, py)
        self.bot.set_angle(theta_1)
        self.mid.set_angle(theta_2)
        self.top.set_angle(theta_3)

    # ------------------------------ Move y-neg
    def y_neg(self, py):
        print("> arm y_neg")
        theta_1, theta_2, theta_3 = self.calculate_inverse_kinematic(0, py)
        self.bot.set_angle(theta_1)
        self.mid.set_angle(theta_2)
        self.top.set_angle(theta_3)

    # ------------------------------ Move to floor - reach ball
    def height_floor(self):
        print("> arm height floor")
        theta_1, theta_2, theta_3 = self.calculate_inverse_kinematic(0, 0)  # need to find (x, y) coordinates
        self.bot.set_angle(theta_1)
        self.mid.set_angle(theta_2)
        self.top.set_angle(theta_3)

    # ------------------------------ Move to height 1 - lowest
    def height_1(self):
        print("> arm height 1")
        theta_1, theta_2, theta_3 = self.calculate_inverse_kinematic(0, 0)  # need to find (x, y) coordinates
        self.bot.set_angle(theta_1)
        self.mid.set_angle(theta_2)
        self.top.set_angle(theta_3)

    # ------------------------------ Move to height 2 - middle
    def height_2(self):
        print("> arm height 2")
        theta_1, theta_2, theta_3 = self.calculate_inverse_kinematic(0, 0)  # need to find (x, y) coordinates
        self.bot.set_angle(theta_1)
        self.mid.set_angle(theta_2)
        self.top.set_angle(theta_3)

    # ------------------------------ Move to height 3 - highest
    def height_3(self):
        print("> arm height 3")
        theta_1, theta_2, theta_3 = self.calculate_inverse_kinematic(0, 0)  # need to find (x, y) coordinates
        self.bot.set_angle(theta_1)
        self.mid.set_angle(theta_2)
        self.top.set_angle(theta_3)

    # ------------------------------ Get angles
    def calculate_inverse_kinematic(self, px, py):
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


