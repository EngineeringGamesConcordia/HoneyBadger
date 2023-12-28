#from motors import dcMotor
import board
import busio
import RPi.GPIO as GPIO
from time import sleep

class Vacuum:
    #def __init__(self, IN1, IN2, PWM):
    def __init__(self, IN1):
        print("Init vacuum")
        #self.vacuum = dcMotor(IN1, IN2, PWM)
        GPIO.setup(self.IN1, GPIO.OUT)
    # ------------------------------ Start vacuum
    def start_vacuum(self):
        print("> vacuum start")
        GPIO.output(self.IN1, GPIO.HIGH)
        sleep(0.01)
        #self.vacuum.cw()

    # ------------------------------ Stop vacuum
    def stop_vacuum(self):
        print("> vacuum stop")
        GPIO.output(self.IN1, GPIO.LOW)
        #self.vacuum.ccw()