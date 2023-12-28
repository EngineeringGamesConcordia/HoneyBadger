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

        #code below to get rid of
class stepperMotor:
    def __init__(self, dir, step, speed): #should be 19, 26,.0108
        self.dir = dir
        self.step = step
        self.delay = speed #.0208 #speed
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dir, GPIO.OUT)
        GPIO.setup(self.step, GPIO.OUT)
        
    def cw(self):
        GPIO.output(self.dir, 0)
        GPIO.output(self.step, GPIO.HIGH)
        sleep(self.delay)
        GPIO.output(self.step, GPIO.LOW)
        sleep(self.delay)
        
    def ccw(self):
        GPIO.output(self.dir, 1)
        GPIO.output(self.step, GPIO.HIGH)
        sleep(self.delay)
        GPIO.output(self.step, GPIO.LOW)
        sleep(self.delay)
    #no need for stop function has works by step
        