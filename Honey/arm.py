from motors import servoMotor
from numpy import *

# reference: https://www.youtube.com/watch?v=3rFaZMvgNe8

# a1: displacement in the z-direction of joint one from the ground (i.e height)
# a2: displacement from the axes of rotation from Motor 1 to Motor 2
# a3: displacement in the z-direction from joint 1 to joint 2 (in this case 0 because both are at the same height)
# a4:  the displacement from the axis of rotation from Motor 2 to the tool tip

# motor pins
BOT = 0
TOP = 0

class Arm:
    def __int__(self):
        print("Init arm")
        self.bot = servoMotor(BOT)
        self.top = servoMotor(TOP)

    # ------------------------------ Move x-pos
    def x_pos(self, px):
        print("> arm x_pos")
        theta_1, theta_2 = self.calculate_inverse_kinematic(px, 0)
        self.bot.set_angle(theta_1)
        self.top.set_angle(theta_1)

    # ------------------------------ Move x-neg
    def x_neg(self, px):
        print("> arm x_neg")
        theta_1, theta_2= self.calculate_inverse_kinematic(px, 0)
        self.bot.set_angle(theta_1)
        self.top.set_angle(theta_2)

    # ------------------------------ Move y-pos
    def y_pos(self, py):
        print("> arm y_pos")
        theta_1, theta_2 = self.calculate_inverse_kinematic(0, py)
        self.bot.set_angle(theta_1)
        self.top.set_angle(theta_2)

    # ------------------------------ Move y-neg
    def y_neg(self, py):
        print("> arm y_neg")
        theta_1, theta_2= self.calculate_inverse_kinematic(0, py)
        self.bot.set_angle(theta_1)
        self.top.set_angle(theta_2)

    # ------------------------------ Move to floor - reach ball
    def height_floor(self):
        print("> arm height floor")
        theta_1, theta_2= self.calculate_inverse_kinematic(0, 0)  # need to find (x, y) coordinates
        self.bot.set_angle(theta_1)
        self.top.set_angle(theta_2)

    # ------------------------------ Get angles
    def calculate_inverse_kinematic(self, px, py):
        # lenghts of links in cm -- need to be changed ofc
        a1 = 6.2  # length of link a1 in cm
        a2 = 5.2  # length of link a2 in cm
        a3 = 0  # length of link a3 in cm
        a4 = 7  # length of link a4 in cm

        # Equations for Inverse kinematics
        r1 = sqrt(px ** 2 + py ** 2)  # eqn 1
        phi_1 = arccos((a4 ** 2 - a2 ** 2 - r1 ** 2) / (-2 * a2 * r1))  # eqn 2
        phi_2 = arctan2(py, px)  # eqn 3
        theta_1 = rad2deg(phi_2 - phi_1)  # eqn 4 converted to degrees

        phi_3 = arccos((r1 ** 2 - a2 ** 2 - a4 ** 2) / (-2 * a2 * a4))
        theta_2 = 180 - rad2deg(phi_3)

        # print('theta one: ', theta_1)
        # print('theta two: ', theta_2)

        return theta_1, theta_2


