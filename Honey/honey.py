import os
import threading
import RPi.GPIO as GPIO
import time   
import math

from time import sleep
from adafruit_servokit import ServoKit

from controller import HoneyController
from arm import Arm
from drive import Drive
from relay import Relay
from automation import Automation
from motors import *

def restart():
    os.system('sudo reboot')


def threadFunction(controller):
    print("Spawning controller thread")
    controller.listen()  # set on_disconnect=restart for final usage

GPIO.setmode(GPIO.BCM)

kit = ServoKit(channels=16)
angles = [80,80]
base_stepper = stepperMotor(19,26,.0108)#dir, step, speed
arm1 = Arm(base_stepper, kit, angles)
relay1 = Relay(23, 24)
front_left = dcMotor(22, 27, 17) #en1, en2, pwm
front_right = dcMotor(6, 13, 25)
back_left = dcMotor(7, 1, 8)
back_right = dcMotor(20, 21, 16)
drivesys = Drive(front_left, front_right, back_left, back_right)
automation1 = Automation()

def ticks():#works
    while(True):
        times = time.time()
        floatingTime = float(times)
        if(math.floor(floatingTime*1000)%10==0):
            controller.checker()


try:
    controller = HoneyController(arm1, drivesys, relay1, automation1, interface="/dev/input/js0", connecting_using_ds4drv=False)
    t1 = threading.Thread(target=threadFunction, args=(controller,))
    t2 = threading.Thread(target=ticks)

    t1.start() 
    t2.start()
    t1.join()
    t2.join()
except KeyboardInterrupt:
    GPIO.cleanup()
