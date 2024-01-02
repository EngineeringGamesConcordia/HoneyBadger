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
angles = [90, 80, 80]
arm1 = Arm(kit, angles)
relay1 = Relay(23, 24)
front_left = dcMotor(22, 27, 17) #en1, en2, pwm
front_right = dcMotor(13, 6, 25)
back_left = dcMotor(7, 1, 8)
back_right = dcMotor(20, 21, 16)
drivesys = Drive(front_left, front_right, back_left, back_right)
automation1 = Automation()

def ticks():#works
    while(True):
        times = time.time()
        floatingTime = float(times)
        if(math.floor(floatingTime*2000)%10==0):
            controller.checker()

def on_L3_press(self):
    self.l3Counter += 1
    print("L3Counter is at "+ str(self.l3Counter))
    if(self.l3Counter >1):
    self.l3Cycle = not (self.l3Cycle);
    print("Ball Pos is"+ str(self.l3Cycle))
        if(self.l3Cycle):
            print("Ball Position")
            arm.defaultPosition()
            sleep(10)
            arm.stepper_servo = 60
            arm.kit.servo[0].angle = arm.stepper_servo                  
            sleep(10)
            arm.ballPosition();
        else:
            print("Launch Position")
            arm.defaultPosition()
            sleep(10)
            arm.stepper_servo  = 90
            arm.kit.servo[0].angle = arm.stepper_servo
            sleep(10)
            arm.launchPosition();

try:
    controller = HoneyController(arm1, drivesys, relay1, automation1, interface="/dev/input/js0", connecting_using_ds4drv=False)
    t1 = threading.Thread(target=threadFunction, args=(controller,))
    t2 = threading.Thread(target=ticks)
    t3 = threading.Thread(target=on_L3_press)

    t1.start() 
    t2.start()
    t3.start()
    t1.join()
    t2.join()
    t3.join()
except KeyboardInterrupt:
    GPIO.cleanup()