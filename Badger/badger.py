import os
import threading
import RPi.GPIO as GPIO

from time import sleep
from pcaBoard import PcaBoard
from controller import BadgerController
from automation import Automation
from motors import stepperMotor

from arm import Arm
from drive import Drive
from vacuum import Vacuum


def restart():
    os.system('sudo reboot')


def threadFunction(controller):
    print("Spawning controller thread")
    controller.listen(timeout=60)  # set on_disconnect=restart for final usage


GPIO.setmode(GPIO.BCM)
pca = PcaBoard()

#TODO test and fix parameters

base_servo = pca.addServo()
elbow_servo = pca.addServo()
wrist_r_servo = pca.addServo()
wrist_ud_servo = pca.addServo()
claw_servo = pca.addServo()

left_track = pca.addMotor()
right_track = pca.addMotor()

base_stepper = stepperMotor()

