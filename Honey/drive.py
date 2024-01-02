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
    def move_front(self,speed):
        self.speed = speed
        print("> drive move front")
        self.front_left.cw(self.speed)
        self.front_right.ccw(self.speed)
        self.back_left.cw(self.speed)
        self.back_right.ccw(self.speed)

    # ------------------------------ Drive back
    def move_back(self,speed):
        self.speed = speed
        print("> drive move back")
        self.front_left.ccw(self.speed)
        self.front_right.cw(self.speed)
        self.back_left.ccw(self.speed)
        self.back_right.cw(self.speed)
        
    # ------------------------------ Drive left
    def move_left(self,speed):
        self.speed = speed
        print("> drive move left")
        self.front_left.ccw(self.speed)
        self.front_right.cw(self.speed)
        self.back_left.ccw(self.speed)
        self.back_right.cw(self.speed)

    # ------------------------------ Drive right
    def move_right(self,speed):
        self.speed = speed
        print("> drive move right")
        self.front_left.cw(self.speed)
        self.front_right.ccw(self.speed)
        self.back_left.cw(self.speed)
        self.back_right.ccw(self.speed)
        
    def move_stop(self):
        self.front_left.stop()
        self.front_right.stop()
        self.back_left.stop()
        self.back_right.stop()
        
