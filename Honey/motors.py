import RPi.GPIO as GPIO
from time import sleep


class dcMotor:
    GPIO.setmode(GPIO.BOARD)

    def __init__(self, in1, in2, pwmPin):
        self.in1 = in1
        self.in2 = in2
        self.pwmPin = pwmPin
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.pwmPin, GPIO.OUT)

    def forward(self):
        GPIO.output(self.in1, GPIO.HIGH)
        sleep(5)
        GPIO.output(self.in2, GPIO.LOW)
        sleep(1)
        GPIO.cleanup()

    def backward(self):
        GPIO.output(self.in1, GPIO.LOW)
        sleep(5)
        GPIO.output(self.in2, GPIO.HIGH)
        sleep(1)
        GPIO.cleanup()

    def stop(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.cleanup()


class stepperMotor:
    def __init__(self, dir, step, speed): #should be 19, 26,.0108
        self.dir = dir
        self.step = step
        self.delay = speed #.0208 #speed
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dir, GPIO.OUT)
        GPIO.setup(self.step, GPIO.OUT)
    def cw(self):
        #could have a small for loop which will make it do a few movement
        GPIO.output(self.dir, 1)
        GPIO.output(self.step, GPIO.HIGH)
        sleep(self.delay)
        GPIO.output(self.step, GPIO.LOW)
        sleep(self.delay)
        
    def ccw(self):
        GPIO.output(self.dir, 0)
        GPIO.output(self.step, GPIO.HIGH)
        sleep(self.delay)
        GPIO.output(self.step, GPIO.LOW)
        sleep(self.delay)
    #no need for stop function has works by step
        