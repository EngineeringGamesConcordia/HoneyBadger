from motors import dcMotor

FRONT_LEFT_IN1 = 0
FRONT_LEFT_IN2 = 0
FRONT_LEFT_PWM = 0

FRONT_RIGHT_IN1 = 0
FRONT_RIGHT_IN2 = 0
FRONT_RIGHT_PWM = 0

BACK_LEFT_IN1 = 0
BACK_LEFT_IN2 = 0
BACK_LEFT_PWM = 0

BACK_RIGHT_IN1 = 0
BACK_RIGHT_IN2 = 0
BACK_RIGHT_PWM = 0

class Drive:
    def __int__(self):
        print("Init drive")
        self.front_left = dcMotor(FRONT_LEFT_IN1, FRONT_LEFT_IN2, FRONT_LEFT_PWM)
        self.front_right = dcMotor(FRONT_RIGHT_IN1, FRONT_RIGHT_IN2, FRONT_RIGHT_PWM)
        self.back_left = dcMotor(BACK_LEFT_IN1, BACK_LEFT_IN2, BACK_LEFT_PWM)
        self.back_right = dcMotor(BACK_RIGHT_IN1, BACK_RIGHT_IN2, BACK_RIGHT_PWM)

    # ------------------------------ Drive front
    def move_front(self,speedx,speedy):
        print("> drive move front")
        self.front_left.forward()
        self.front_right.forward()
        self.back_left.forward()
        self.back_right.forward()

    # ------------------------------ Drive back
    def move_back(self,speedx,speedy):
        print("> drive move back")
        self.front_left.backward()
        self.front_right.backward()
        self.back_left.backward()
        self.back_right.backward()

    # ------------------------------ Drive left
    def move_left(self,speedx,speedy):
        print("> drive move left")
        self.front_left.backward()
        self.front_right.forward()
        self.back_left.backward()
        self.back_right.forward()

    # ------------------------------ Drive right
    def move_right(self,speedx,speedy):
        print("> drive move right")
        self.front_left.forward()
        self.front_right.backward()
        self.back_left.forward()
        self.back_right.backward()
