from pyPS4Controller.controller import Controller
from controller import BadgerController
import time

class MyController(Controller):

    time = round(time.perf_counter()*1)
    print(time)
    while(True):
        armX = (BadgerController.getLastValueArmX)
        armX =str(armX)
        armX = int(armX,16)
        
        armY = (BadgerController.getLastValueArmY) 
        armY = str(armY)
        armY = int(armY,16)
        
        driveX = (BadgerController.getLastValueDriveX)
        driveX = str(driveX)
        driveX = int(driveX,16)

        driveY = (BadgerController.getLastValueDriveY)
        driveY = str(driveY)
        driveY = int(driveY,16)
       
        
        clawOpen = (BadgerController.getLastValueOpenClaw) 
        clawOpen = str(clawOpen)
        clawOpen = int(clawOpen, 16)
    
        
        clawClose = (BadgerController.getLastValueOpenClaw) 
        clawClose = str(clawClose)
        clawClose = int(clawClose,16)
   
        
        if(time%2==0):
            print("WompWomp value of arm X: "+ str(armX) )
            print("WompWomp value of arm Y: "+ str(armY) )
            print("WompWomp value of drive X: "+ str(driveX) )
            print("WompWomp value of drive Y: "+ str(driveY) )
            print("WompWomp value of claw open: "+ str(clawOpen) )
            print("WompWomp value of claw close: "+ str(clawClose) )
            
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_x_press(self):
        print("Hello world")

    def on_x_release(self):
        print("Goodbye world")


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
# you can start listening before controller is paired, as long as you pair it within the timeout window
controller.listen(timeout=60)