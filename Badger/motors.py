import board
import busio
import RPi.GPIO as GPIO
from time import sleep

class dcMotor:

    def __init__(self, in1, in2, pwmPin):
        self.in1 = in1
        self.in2 = in2
        self.pwmPin = pwmPin
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.pwmPin, GPIO.OUT)

    def cw(self):
        GPIO.output(self.in1, GPIO.HIGH)
        sleep(0.01)
        GPIO.output(self.in2, GPIO.LOW)
        sleep(0.01)

    def ccw(self):
        GPIO.output(self.in1, GPIO.LOW)
        sleep(0.01)
        GPIO.output(self.in2, GPIO.HIGH)
        sleep(0.01)

    def stop(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)

        #code below to get rid of
class stepperMotor:
    DIR = 19   # Direction GPIO Pin
    STEP = 26  # Step GPIO Pin
    CW = 1     # Clockwise Rotation
    CCW = 0    # Counterclockwise Rotation
    SPR = 60   # Steps per Revolution (360 / 7.5)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(DIR, GPIO.OUT)
    GPIO.setup(STEP, GPIO.OUT)
    step_count = SPR
    delay = .0108
        