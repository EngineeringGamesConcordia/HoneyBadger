from controller import HoneyController
from arm import Arm
from drive import Drive
from Honey.Vacuum import Vacuum
from automation import Automation

arm = Arm()
drive = Drive()
vacuum = Vacuum()
automation = Automation()

controller = HoneyController(arm, drive, vacuum, automation, "/dev/input/js0", False)