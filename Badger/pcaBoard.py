import RPi.GPIO as GPIO
import time

class Servo:
    def __init__(self, pin, init_angle=0, min_angle=0, max_angle=270):
        print("initializing new servo on pin " + str(pin) +
              "init_angle: " + str(init_angle) +
              "min_angle: " + str(min_angle) +
              "max_angle: " + str(max_angle))

        self.pin = pin
        self.min_angle = min_angle
        self.max_angle = max_angle
