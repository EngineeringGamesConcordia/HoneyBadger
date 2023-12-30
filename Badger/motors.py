import board
import busio
import RPi.GPIO as GPIO
from time import sleep

class dcMotor:
    def __init__(self, fpwm, bpwm):
        self.fpwm = fpwm
        self.bpwm = bpwm
        GPIO.setup(self.fpwm, GPIO.OUT)
        GPIO.setup(self.bpwm, GPIO.OUT)
        GPIO.output(self.fpwm, GPIO.LOW)
        GPIO.output(self.bpwm, GPIO.LOW)
        

    def cw(self):
        GPIO.output(self.bpwm, GPIO.LOW)
        GPIO.output(self.fpwm, GPIO.HIGH)

    def ccw(self):
        GPIO.output(self.fpwm, GPIO.LOW)
        GPIO.output(self.bpwm, GPIO.HIGH)

    def stop(self):
        GPIO.output(self.fpwm, GPIO.LOW)
        GPIO.output(self.bpwm, GPIO.LOW)
        