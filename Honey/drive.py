from motors import dcMotor
from math import ceil

class Drive:
    def __init__(self, front_left, front_right, back_left, back_right):
        print("Init drive")
        self.front_left = front_left
        self.front_right = front_right
        self.back_left = back_left
        self.back_right = back_right

    # ------------------------------ Drive front
    def move_front(self,speedx,speedy):
        print("> drive move front")
        self.front_left.cw()
        self.front_right.cw()
        self.back_left.cw()
        self.back_right.cw()

    # ------------------------------ Drive back
    def move_back(self,speedx,speedy):
        print("> drive move back")
        self.front_left.ccw()
        self.front_right.ccw()
        self.back_left.ccw()
        self.back_right.ccw()
        
    # ------------------------------ Drive left
    def move_left(self,speedx,speedy):
        print("> drive move left")
        self.front_left.ccw()
        self.front_right.cw()
        self.back_left.ccw()
        self.back_right.cw()

    # ------------------------------ Drive right
    def move_right(self,speedx,speedy):
        print("> drive move right")
        self.front_left.cw()
        self.front_right.ccw()
        self.back_left.cw()
        self.back_right.ccw()
