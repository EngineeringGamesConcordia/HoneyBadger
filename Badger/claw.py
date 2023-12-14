from motors import servoMotor

PIN = 0

class Claw:
    def __init__(self):
        print("Init claw")
        self.claw = servoMotor(PIN)

# ------------------------------ Claw open
def open_claw(self):
    print("> claw open")
    self.claw.set_angle(90)
    
# ------------------------------ Claw close
def close_claw(self):
    print("> claw close")
    self.claw.set_angle(0)

    
    