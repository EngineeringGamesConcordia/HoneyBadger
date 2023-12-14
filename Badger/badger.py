from controller import BadgerController
from arm import Arm
from claw import Claw
from drive import Drive
from vacuum import Vacuum
from wrist import Wrist
from automation import Automation

arm = Arm()
claw = Claw()
drive = Drive()
vacuum = Vacuum()
wrist =  Wrist()
automation = Automation()

controller = BadgerController(arm, claw, drive, vacuum, wrist, automation, "/dev/input/js0", False)