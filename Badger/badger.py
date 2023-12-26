import os
import threading
import RPi.GPIO as GPIO

from time import sleep
from adafruit_servokit import ServoKit
from controller import BadgerController
from automation import Automation
from motors import stepperMotor
from motors import dcMotor
from arm import Arm
from vacuum import Vacuum
from drive import Drive


def restart():
    os.system('sudo reboot')


def threadFunction(controller):
    print("Spawning controller thread")
    controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
    controller.listen(timeout=60)  # set on_disconnect=restart for final usage


GPIO.setmode(GPIO.BCM)

#TODO test and fix parameters
kit = ServoKit(channels=16)
#base_stepper = stepperMotor(#def __init__(self, pin1, pin2, pin3, pin4):
arm1 = Arm(base_stepper, kit.servo[0], kit.servo[1], kit.servo[2], kit.servo[3], kit.servo[4])
#vacuum1 = Vacuum(#def __init__(self, IN1, IN2, PWM):
#left_track = dcMotor(#def __init__(self, in1, in2, pwmPin):
#right_track = dcMotor(#def __init__(self, in1, in2, pwmPin):
drivesys = Drive(left_track, right_track)

#controller = BadgerController(arm1, arm1.claw_servo, drivesys, vacuum1, arm1.wrist_r_servo, #automation, interface, ds4drv)


