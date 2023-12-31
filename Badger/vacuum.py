#from motors import dcMotor
import RPi.GPIO as GPIO
from time import sleep

class Vacuum:
    def __init__(self, IN1):
        self.IN1 = IN1
        print("Init relay")
        GPIO.setup(self.IN1, GPIO.OUT)
    # ------------------------------ Start vacuum
    def start_vacuum(self):
        print("> relay start")
        GPIO.output(self.IN1, GPIO.HIGH)
        sleep(0.01)

    # ------------------------------ Stop vacuum
    def stop_vacuum(self):
        print("> relay stop")
        GPIO.output(self.IN1, GPIO.LOW)
