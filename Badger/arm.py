from motors import servoMotor

BOT = 0
MID = 0
TOP = 0

class Arm:
    def __int__(self):
        print("Init arm")
        self.bot = servoMotor(BOT)
        self.mid = servoMotor(MID)
        self.top = servoMotor(TOP)

    # ------------------------------ Move x-pos
    def x_pos(self):
        print("> arm x_pos")

    # ------------------------------ Move x-neg
    def x_neg(self):
        print("> arm x_neg")

    # ------------------------------ Move y-pos
    def y_pos(self):
        print("> arm y_pos")

    # ------------------------------ Move y-neg
    def y_neg(self):
        print("> arm y_neg")

    # ------------------------------ Move to floor - reach ball

    def height_floor(self):
        print("> arm height floor")

    # ------------------------------ Move to height 1 - lowest
    def height_1(self):
        print("> arm height 1")

    # ------------------------------ Move to height 2 - middle
    def height_2(self):
        print("> arm height 2")

    # ------------------------------ Move to height 3 - highest

    def height_3(self):
        print("> arm height 3")