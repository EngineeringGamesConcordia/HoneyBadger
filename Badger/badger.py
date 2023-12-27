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
import time


def restart():
    os.system('sudo reboot')


def threadFunction(controller):
    print("Spawning controller thread")
    controller.listen()  # set on_disconnect=restart for final usage

GPIO.setmode(GPIO.BCM)

#TODO test and fix parameters
kit = ServoKit(channels=16)
angles = [80,80,80,0,20]
base_stepper = stepperMotor(25, 8, 7, 12)
arm1 = Arm(base_stepper, kit, angles)
vacuum1 = Vacuum(10, 9, 11)
left_track = dcMotor(16, 20, 21)
right_track = dcMotor(5, 6, 13)
drivesys = Drive(left_track, right_track)
automation1 = Automation()


controller = BadgerController(arm1, arm1.claw_servo, drivesys, vacuum1, arm1.wrist_r_servo, automation1, interface="/dev/input/js0", connecting_using_ds4drv=False)
while(True):
    time = time.time()
    floatingTime = float(time)
    print(floatingTime)
    if(round(floatingTime)%2==0):
        controller.listen()
        controller.checker()