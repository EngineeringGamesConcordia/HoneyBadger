from arm import Arm
from drive import Drive
from vacuum import Vacuum
from motors import dcMotor
from motors import stepperMotor
from controller import BadgerController
from time import sleep

class Automation:
    def __init__(self):
        print("Init automation")
        
    def start(self):
        print("> automation start")
    