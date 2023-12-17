from motors import dcMotor

IN1 = 0
IN2 = 0
PWM = 0

# the spinwill duh

class Throw:
    def __int__(self):
        print("Init throw")
        self.throw = dcMotor(IN1, IN2, PWM)

    # ------------------------------ Start throw
    def start_vacuum(self):
        print("> throw start")
        self.throw.forward()

    # ------------------------------ Stop throw
    def stop_vacuum(self):
        print("> throw stop")
        self.throw.stop()