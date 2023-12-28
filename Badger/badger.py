import os
import threading
import RPi.GPIO as GPIO

from time import sleep
from adafruit_servokit import ServoKit
from controller import BadgerController
from automation import Automation
from motors import *

from arm import Arm
from vacuum import Vacuum
from drive import Drive
import time   
import math


def restart():
    os.system('sudo reboot')


def threadFunction(controller):
    print("Spawning controller thread")
    controller.listen()  # set on_disconnect=restart for final usage

GPIO.setmode(GPIO.BCM)

#TODO test and fix parameters
kit = ServoKit(channels=16)
angles = [80,80,40,80,20]
base_stepper = stepperMotor()#to be fixed later
arm1 = Arm(base_stepper, kit, angles)
vacuum1 = Vacuum(22)
left_track = dcMotor(5, 6) #rpwm = forward mioght have to swap it the pin if going oposite direction
right_track = dcMotor(13, 19)
drivesys = Drive(left_track, right_track)
automation1 = Automation()
#send the value from the contrller to the arm
def ticks():#works
    while(True):
        times = time.time()
        floatingTime = float(times)
        if(math.floor(floatingTime*100)%10==0):
            controller.checker()


try:
    controller = BadgerController(arm1, arm1.claw_servo, drivesys, vacuum1, arm1.wrist_r_servo, automation1, interface="/dev/input/js0", connecting_using_ds4drv=False)
    t1 = threading.Thread(target=threadFunction, args=(controller,))
    t2 =  threading.Thread(target=ticks)

    t1.start() 
    t2.start()
    t1.join()
    t2.join()
except KeyboardInterrupt:
    GPIO.cleanup()
    