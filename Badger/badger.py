from controller import BadgerController
from arm import Arm
from claw import Claw
from drive import Drive
from vacuum import Vacuum
from automation import Automation

arm = Arm()
claw = Claw()
drive = Drive()
vacuum = Vacuum()
automation = Automation()

controller = BadgerController(arm, claw, drive, vacuum, automation, "/dev/input/js0", False)