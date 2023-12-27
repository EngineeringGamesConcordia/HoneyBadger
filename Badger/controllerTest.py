from pyPS4Controller.controller import Controller
from controller import BadgerController
import time

class MyController(Controller):

    time = time.perf_counter()


   
    print(time)    
    if(time%2==0):
        armX = (BadgerController.getLastValueArmX)
        armX = int(str(armX))
        
        armY = (BadgerController.getLastValueArmY) 
        armY = int(str(armY))
        
        driveX = (BadgerController.getLastValueDriveX)
        driveX = str(driveX)
        driveX = int(driveX,16)

        driveY = (BadgerController.getLastValueDriveY)
        driveY = int(str(driveY))
       
        
        clawOpen = (BadgerController.getLastValueOpenClaw) 
        clawOpen = int(str(clawOpen))
    
        
        clawClose = (BadgerController.getLastValueOpenClaw) 
        clawClose = int(str(clawClose))    
        print("WompWomp value of arm X: "+ str(armX) )
        print("WompWomp value of arm Y: "+ str(armY) )
        print("WompWomp value of drive X: "+ str(driveX) )
        print("WompWomp value of drive Y: "+ str(driveY) )
        print("WompWomp value of claw open: "+ str(clawOpen) )
        print("WompWomp value of claw close: "+ str(clawClose) )
    print(time)        
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_x_press(self):
        print("Hello world")

    def on_x_release(self):
        print("Goodbye world")


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
# you can start listening before controller is paired, as long as you pair it within the timeout window
controller.listen(timeout=60)