import RPi.GPIO as GPIO
from time import sleep

class Relay:
    def __init__(self, IN1, IN2):
        self.IN1 = IN1
        self.IN2 = IN2
        print("Init relay")
        GPIO.setup(self.IN1, GPIO.OUT)
        GPIO.setup(self.IN2, GPIO.OUT)
    # ------------------------------ Start vacuum
    def start_vacuum(self):
        print("> relay,vacuum start")
        GPIO.output(self.IN1, GPIO.HIGH)

    # ------------------------------ Stop vacuum
    def stop_vacuum(self):
        print("> relay,vacuum stop")
        GPIO.output(self.IN1, GPIO.LOW)
        
    # ------------------------------ Start throw
    def start_throw(self):
        print("> relay,throw start")
        GPIO.output(self.IN2, GPIO.HIGH)

    # ------------------------------ Stop throw
    def stop_throw(self):
        print("> relay,throw stop")
        GPIO.output(self.IN2, GPIO.LOW)
