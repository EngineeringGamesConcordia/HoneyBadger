import os
import threading
import RPi.GPIO as GPIO


from adafruit_servokit import ServoKit
from automation import Automation
from motors import *

from controller import HoneyController
from arm import Arm
from drive import Drive
from relay import Relay
from automation import Automation

import time   
import math
from time import sleep



arm = Arm()
drive = Drive()
vacuum = Relay()
flying_wheel = Relay()
automation = Automation()

controller = HoneyController(arm, drive, vacuum, automation, "/dev/input/js0", False)