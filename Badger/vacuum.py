from motors import dcMotor

IN1 = 0
IN2 = 0
PWM = 0

class Vacuum:
    def __init__(self, IN1, IN2, PWM):
        print("Init vacuum")
        self.vacuum = dcMotor(IN1, IN2, PWM)

    # ------------------------------ Start vacuum
    def start_vacuum(self):
        print("> vacuum start")
        self.vacuum.cw()

    # ------------------------------ Stop vacuum
    def stop_vacuum(self):
        print("> vacuum stop")
        self.vacuum.ccw()