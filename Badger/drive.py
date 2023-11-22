from time import sleep
from motors import dcMotor
import RPi.GPIO as GPIO

DC_MOTOR_LEFT_IN1 = 0
DC_MOTOR_LEFT_IN2 = 0
DC_MOTOR_LEFT_PWM = 0
DC_MOTOR_RIGHT_IN1 = 0
DC_MOTOR_RIGHT_IN2 = 0
DC_MOTOR_RIGHT_PWM = 0

class Drive:
    def __int__(self):
        print("Init drive")
        self.left = dcMotor(DC_MOTOR_LEFT_IN1, DC_MOTOR_LEFT_IN2, DC_MOTOR_LEFT_PWM)
        self.right = dcMotor(DC_MOTOR_RIGHT_IN1, DC_MOTOR_RIGHT_IN2, DC_MOTOR_RIGHT_PWM)

    # ------------------------------ Drive front
    def move_front(self):
        print("> drive move front")
        self.left.forward(100)
        self.right.forward(100)

    # ------------------------------ Drive back
    def move_back(self):
        print("> drive move back")
        self.left.backward(100)
        self.right.backward(100)

    # ------------------------------ Drive left
    def move_left(self):
        print("> drive move left")
        self.left.backward(100)
        self.right.forward(100)

    # ------------------------------ Drive right
    def move_right(self):
        print("> drive move right")
        self.left.forward(100)
        self.right.backward(100)
