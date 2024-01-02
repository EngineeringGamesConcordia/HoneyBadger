import numpy as np
import RPi.GPIO as GPIO
from time import sleep
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)
CONTROLLER_SCALE = 2**15
BIG_SERVO_SCALE = 1/(2**18)
SMALL_SERVO_SCALE = 1/(2**18)
CLAW_SCALE = 1/(2**18)
KINEMATIC_SCALE = 2.5/(2**20)

moveVal = 0.1
l1 = 22
l2 = 21.16
offset2 = 6
offset_x= 0
offset_y= 0
px = 0
py = 0

def adjust_to_limits(theta, theta_min, theta_max):
    # Adjust the joint angle to stay within limits
    adjusted_theta = (theta - theta_min) % (theta_max - theta_min) + theta_min
    return adjusted_theta

def forward_kinematics(theta1, theta2):
    x = offset_x + l1 * np.cos(theta1) + l2 * np.cos(theta1 + theta2)
    y = offset_y + l1 * np.sin(theta1) + l2 * np.sin(theta1 + theta2) - offset2
    return x, y


# ------------------------------ Get angles
def calculate_inverse_kinematic(x_target, y_target, initial_theta1, initial_theta2):
    
    print ("Initial theta1 = " + str(initial_theta1))
    print ("Initial theta2 = " + str(initial_theta2))
    
    def calculate_cost(theta1, theta2, initial_theta1, initial_theta2):
        return np.sqrt((theta1 - initial_theta1)**2 + (theta2 - initial_theta2)**2)
        #return np.abs(theta1 - initial_theta1) + np.abs(theta2 - initial_theta2)
        
    theta = np.arctan2(y_target, x_target)
    x_adjusted = (x_target - (offset2 * np.cos(theta)) - offset_x)
    y_adjusted = (y_target - (offset2 * np.sin(theta)) - offset_y)
    
    if (y_adjusted < 0.0):
        y_adjusted = 0
    
    D = (x_adjusted**2 + y_adjusted**2 - l1**2 - l2**2) / (2 * l1 * l2)
    
    
    if np.abs(D) > 1:
        print("No solution for given x, y.")
        return initial_theta1, initial_theta2
    
    theta2_1 = np.arctan2(np.sqrt(1 - D**2), D)
    theta2_2 = -np.arctan2(np.sqrt(1 - D**2), D)
    
    theta1_1 = theta - np.arctan2(l2 * np.sin(theta2_1), l1 + l2 * np.cos(theta2_1))
    theta1_2 = theta - np.arctan2(l2 * np.sin(theta2_2), l1 + l2 * np.cos(theta2_2))
    
    # Calibration factors
    calibration_factor_theta1 = np.deg2rad(-20)  # Adjust as needed
    calibration_factor_theta2 = np.deg2rad(-20)  # Adjust as needed

    # Apply calibration factors
    theta1_1 += calibration_factor_theta1
    theta1_2 += calibration_factor_theta1
    theta2_1 += calibration_factor_theta2
    theta2_2 += calibration_factor_theta2
    
    # Define joint angle limits
    # Define joint angle limits in radians
    theta1_min, theta1_max = np.deg2rad(15), np.deg2rad(160)
    theta2_min, theta2_max = np.deg2rad(10), np.deg2rad(155)

    solutions = ((theta1_1, theta2_1), (theta1_2, theta2_2))
    
    optimal_solution = None
    min_cost = float('inf')

    for sol in solutions:
        theta1, theta2 = np.rad2deg(sol[0]), np.rad2deg(sol[1])
        cost = calculate_cost(sol[0], sol[1],initial_theta1, initial_theta2)

        if (theta1_min <= sol[0] <= theta1_max) and (theta2_min <= sol[1] <= theta2_max) and cost < min_cost and cost <= 200.0:
            min_cost = cost
            optimal_solution = sol

        print("Theta1: {:.2f}, Theta2: {:.2f}, Cost: {:.2f}".format(theta1, theta2, cost))

    if optimal_solution:
        print("\nOptimal Solution:")
        print("Theta1: {:.2f}, Theta2: {:.2f}".format(optimal_solution[0], optimal_solution[1]))
    else:
        print("No optimal solution found within joint angle limits.")
        optimal_solution = (np.deg2rad(initial_theta1), np.deg2rad(initial_theta2))  # Set optimal solution to current angles to prevent damage

    return np.rad2deg(optimal_solution[0]), np.rad2deg(optimal_solution[1])


class Arm:
    global moveVal
    
    def __init__(self, kit, angles):
        global moveVal
        print("Init arm")
        self.initial_theta1 = angles[0]
        self.initial_theta2 = angles[1]
        px, py = forward_kinematics(np.deg2rad(self.initial_theta1), np.deg2rad(self.initial_theta2))
        self.px = px
        self.py = py
        theta_1, theta_2 = calculate_inverse_kinematic(self.px, self.py, self.initial_theta1, self.initial_theta2)
        print ("Here are the initital positions: " + str(px) + "    " + str(py))
        print ("Here are the initital angles: " + str(theta_1) + "    " + str(theta_2))
        self.base_servo = theta_1
        self.elbow_servo = theta_2
        self.wrist_r_servo =  angles[2]
        self.wrist_ud_servo = angles[3]
        self.claw_servo = angles[4]
        self.stepper_servo = angles[5]
        self.kit = kit
        self.kit.servo[0].angle = theta_1 
        self.kit.servo[1].angle = theta_2
        self.kit.servo[2].angle = angles[2]
        self.kit.servo[3].angle = angles[3]
        self.kit.servo[4].angle = angles[4]
        self.kit.servo[5].angle = angles[5]
        self.moveVal = moveVal
        self.SLOW_MODE = False

    # ------------------------------ CLAW MOVEMENTS
    def open_claw(self, val):
        val = CLAW_SCALE * ((((val + CONTROLLER_SCALE) / (2 * CONTROLLER_SCALE)) ** 3) + 2**15)
        print("claw opening - arm")
        self.claw_servo = self.claw_servo + val
        if (self.claw_servo > 175):
            self.claw_servo = 175
        self.kit.servo[4].angle = self.claw_servo

    def close_claw(self, val):
        val = CLAW_SCALE * ((((val + CONTROLLER_SCALE) / (2 * CONTROLLER_SCALE)) ** 3) + 2**15)
        self.claw_servo = self.claw_servo - val
        if (self.claw_servo < 33):
            self.claw_servo = 33
        print("claw closing - arm" + str(self.claw_servo))
        self.kit.servo[4].angle = self.claw_servo
    # ------------------------------ SERVO0 MOVEMENTS
    def serv0_turn_left(self):
        print("> servo0 rotating left")
        self.base_servo = self.base_servo - self.moveVal
        if (self.base_servo < 2):
            self.base_servo = 2
        self.initial_theta1 = self.base_servo
        self.px, self.py = forward_kinematics(np.deg2rad(self.initial_theta1), np.deg2rad(self.initial_theta2))
        self.kit.servo[0].angle = self.base_servo
    def serv0_turn_right(self):
        print("> servo0 rotating right")
        self.base_servo = self.base_servo + self.moveVal
        if (self.base_servo > 175):
            self.base_servo = 175
        self.initial_theta1 = self.base_servo
        self.px, self.py = forward_kinematics(np.deg2rad(self.initial_theta1), np.deg2rad(self.initial_theta2))
        self.kit.servo[0].angle = self.base_servo
    # ------------------------------ SERVO1 MOVEMENTS
    def serv1_turn_left(self):
        print("> servo1 rotating left")
        self.elbow_servo = self.elbow_servo - self.moveVal
        if (self.elbow_servo < 10):
            self.elbow_servo = 10
        self.initial_theta2 = self.elbow_servo
        self.px, self.py = forward_kinematics(np.deg2rad(self.initial_theta1), np.deg2rad(self.initial_theta2))
        self.kit.servo[1].angle = self.elbow_servo
    def serv1_turn_right(self):
        print("> servo1 rotating right")
        self.elbow_servo = self.elbow_servo + self.moveVal
        if (self.elbow_servo > 175):
            self.elbow_servo = 175
        self.initial_theta2 = self.elbow_servo
        self.px, self.py = forward_kinematics(np.deg2rad(self.initial_theta1), np.deg2rad(self.initial_theta2))
        self.kit.servo[1].angle = self.elbow_servo   
    # ------------------------------ ROTATIONAL MOVEMENTS SERV02
    def turn_left(self): 
        print("> wrist rotating left")
        self.wrist_r_servo = self.wrist_r_servo - self.moveVal
        if (self.wrist_r_servo < 5):
            self.wrist_r_servo = 5
        self.kit.servo[2].angle = self.wrist_r_servo

    def turn_right(self):
        print("> wrist rotating right")
        self.wrist_r_servo = self.wrist_r_servo + self.moveVal
        if (self.wrist_r_servo > 175):
            self.wrist_r_servo = 175
        self.kit.servo[2].angle = self.wrist_r_servo

    # ------------------------------ ROTATIONAL MOVEMENTS SERV03
    def go_up(self):
        print("> wrist up")
        self.wrist_ud_servo = self.wrist_ud_servo - self.moveVal
        if (self.wrist_ud_servo < 5):
            self.wrist_ud_servo = 5
        self.kit.servo[3].angle = self.wrist_ud_servo

    def go_down(self):
        print("> wrist down")
        self.wrist_ud_servo = self.wrist_ud_servo + self.moveVal
        if (self.wrist_ud_servo > 155):
            self.wrist_ud_servo = 155
        self.kit.servo[3].angle = self.wrist_ud_servo
    # ------------------------------ ROTATIONAL MOVEMENTS SERV05
    def stepper_turn_right(self):
        print("> stepper servo right")
        self.stepper_servo = self.stepper_servo - self.moveVal
        if (self.stepper_servo < 5):
            self.stepper_servo = 5
        self.kit.servo[5].angle = self.stepper_servo

    def stepper_turn_left(self):
        print("> stepper servo left")
        self.stepper_servo = self.stepper_servo + self.moveVal
        if (self.stepper_servo > 175):
            self.stepper_servo = 175
        self.kit.servo[5].angle = self.stepper_servo   
    # ------------------------------ Move x-pos
    def x_pos(self, val):
        print("> arm22 x_pos")
        val = KINEMATIC_SCALE * ((((val + CONTROLLER_SCALE) / (2 * CONTROLLER_SCALE)) ** 3) + 2**15)
        self.px = self.px - val;
        theta_1, theta_2 = calculate_inverse_kinematic(self.px, self.py, self.initial_theta1, self.initial_theta2)
        print ("px = " + str(self.px))
        print ("theta1 theta2 = " + str(theta_1) + "   " + str(theta_2))
        self.initial_theta1, self.initial_theta2 = theta_1, theta_2
        self.base_servo = theta_1
        self.elbow_servo = theta_2
        self.kit.servo[0].angle = theta_1
        self.kit.servo[1].angle = theta_2

    # ------------------------------ Move x-neg
    def x_neg(self, val):
        print("> arm22 x_neg")
        val = KINEMATIC_SCALE * ((((val + CONTROLLER_SCALE) / (2 * CONTROLLER_SCALE)) ** 3) + 2**15)
        self.px = self.px + val;
        theta_1, theta_2 = calculate_inverse_kinematic(self.px, self.py, self.initial_theta1, self.initial_theta2)
        print ("px = " + str(self.px))
        print ("theta1 theta2 = " + str(theta_1) + "   " + str(theta_2))
        self.initial_theta1, self.initial_theta2 = theta_1, theta_2
        self.base_servo = theta_1
        self.elbow_servo = theta_2
        self.kit.servo[0].angle = theta_1
        self.kit.servo[1].angle = theta_2

    # ------------------------------ Move y-pos
    def y_pos(self, val):
        print("> arm22 y_pos")
        val = KINEMATIC_SCALE * ((((val + CONTROLLER_SCALE) / (2 * CONTROLLER_SCALE)) ** 3) + 2**15)
        self.py = self.py - val;
        theta_1, theta_2 = calculate_inverse_kinematic(self.px, self.py, self.initial_theta1, self.initial_theta2)
        print ("py = " + str(self.py))
        print ("theta1 theta2 = " + str(theta_1) + "   " + str(theta_2))
        self.initial_theta1, self.initial_theta2 = theta_1, theta_2
        self.base_servo = theta_1
        self.elbow_servo = theta_2
        self.kit.servo[0].angle = theta_1
        self.kit.servo[1].angle = theta_2

    # ------------------------------ Move y-neg
    def y_neg(self, val):
        print("> arm22 y_neg")
        val = KINEMATIC_SCALE * ((((val + CONTROLLER_SCALE) / (2 * CONTROLLER_SCALE)) ** 3) + 2**15)
        self.py = self.py + val;
        theta_1, theta_2 = calculate_inverse_kinematic(self.px, self.py, self.initial_theta1, self.initial_theta2)
        print ("py = " + str(self.py))
        print ("theta1 theta2 = " + str(theta_1) + "   " + str(theta_2))
        self.initial_theta1, self.initial_theta2 = theta_1, theta_2
        self.base_servo = theta_1
        self.elbow_servo = theta_2
        self.kit.servo[0].angle = theta_1
        self.kit.servo[1].angle = theta_2
