from motors import servoMotor

PIN = 0


class Wrist:
    def __init__(self):
        print("Init wrist")
        self.wrist = servoMotor(PIN)


# ------------------------------ Wrist turn left
def turn_left(self):
    print("> wrist left")
    self.wrist.set_angle(90)


# ------------------------------ Wrist turn right
def turn_right(self):
    print("> wrist right")
    self.wrist.set_angle(0)


