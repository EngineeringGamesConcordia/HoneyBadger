from pyPS4Controller.controller import Controller

class MyController(Controller):

    time = round(time.perf_counter()*1)
    while(true):
        value = Controller.getConstValue()
        if(time%2==0):
            print("WompWomp value is: "+ constValue)
    def __init__(self, **kwargs):
        Controller.__init__(self, **kwargs)

    def on_x_press(self):
        print("Hello world")

    def on_x_release(self):
        print("Goodbye world")


controller = MyController(interface="/dev/input/js0", connecting_using_ds4drv=False)
# you can start listening before controller is paired, as long as you pair it within the timeout window
controller.listen(timeout=60)