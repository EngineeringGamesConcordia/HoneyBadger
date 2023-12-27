from decimal import ROUND_DOWN, ROUND_FLOOR
from pyPS4Controller.controller import Controller
from controller import BadgerController
import time

class MyController(Controller):
    bc = BadgerController
    time = time.perf_counter()
    floatTime = float(time)

    if round(floatTime) % 2 == 0:
        bc.checker()

        def __init__(self, **kwargs):
            Controller.__init__(self, **kwargs)

        def on_x_press(self):
            print("Hello world")

        def on_x_release(self):
            print("Goodbye world")


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
# you can start listening before the controller is paired, as long as you pair it within the timeout window
controller.listen(timeout=60)