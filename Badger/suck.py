from motors import dcMotor

IN1 = 0
IN2 = 0
PWM = 0

class Suck:
    def __init__(self):
        print("Init suck")
        self.pump = dcMotor(IN1, IN2, PWM)

    # ------------------------------ Start suck
    def start_suck(self):
        print("> suck start suck")
        self.pump.forward(100)

    # ------------------------------ Stop suck
    def stop_suck(self):
        print("> suck stop suck")
        self.pump.stop()