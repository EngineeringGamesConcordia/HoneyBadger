from motors import dcMotor

LEFT_IN1 = 0
LEFT_IN2 = 0
LEFT_PWM = 0
RIGHT_IN1 = 0
RIGHT_IN2 = 0
RIGHT_PWM = 0

class Drive:
    def __int__(self):
        print("Init drive")
        self.left = dcMotor(LEFT_IN1, LEFT_IN2, LEFT_PWM)
        self.right = dcMotor(RIGHT_IN1, RIGHT_IN2, RIGHT_PWM)

    # ------------------------------ Drive front
    def move_front(self):
        print("> drive move front")
        self.left.forward()
        self.right.forward()

    # ------------------------------ Drive back
    def move_back(self):
        print("> drive move back")
        self.left.backward()
        self.right.backward()

    # ------------------------------ Drive left
    def move_left(self):
        print("> drive move left")
        self.left.backward()
        self.right.forward()

    # ------------------------------ Drive right
    def move_right(self):
        print("> drive move right")
        self.left.forward()
        self.right.backward()
