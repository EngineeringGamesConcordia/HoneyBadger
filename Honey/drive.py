from motors import dcMotor
from math import ceil

class Drive:
    def __init__(self, front_left, front_right, back_left, back_right):
        print("Init drive")
        self.front_left = front_left
        self.front_right = front_right
        self.back_left = back_left
        self.back_right = back_right
    
    def convert(self,speedx,speedy):
        self.speedx = (speedx/2**15) # scaling them to 0-1
        self.speedy = (speedy/2**15)
        self.wheel_radius = 0.04 #80mm wheel
        self.honey_geometry = (0.255+0.23) #25.5cm lenght and 23cm wide
        self.front_left_speed = 0

    # ------------------------------ Drive front
    def move_front(self,speedx,speedy):
        print("> drive move front")
        self.front_left.cw(speedx)
        self.front_right.ccw(speedx)
        self.back_left.cw(speedx)
        self.back_right.ccw(speedx)

    # ------------------------------ Drive back
    def move_back(self,speedx,speedy):
        print("> drive move back")
        self.front_left.ccw(speedy)
        self.front_right.cw(speedy)
        self.back_left.ccw(speedy)
        self.back_right.cw(speedy)
        
    # ------------------------------ Drive left
    def move_left(self,speedx,speedy):
        print("> drive move left")
        self.front_left.ccw(speedy)
        self.front_right.ccw(speedx)
        self.back_left.cw(speedy)
        self.back_right.cw(speedx)

    # ------------------------------ Drive right
    def move_right(self,speedx,speedy):
        print("> drive move right")
        self.front_left.cw(speedx)
        self.front_right.cw(speedy)
        self.back_left.ccw(speedx)
        self.back_right.ccw(speedy)
        
    def turn_left(self,speed):
        print("> drive move right")
        self.front_left.cw(speed)
        self.front_right.cw(speed)
        self.back_left.cw(speed)
        self.back_right.cw(speed)
        
    def turn_right(self,speed):
        print("> drive move right")
        self.front_left.ccw(speed)
        self.front_right.ccw(speed)
        self.back_left.ccw(speed)
        self.back_right.ccw(speed)
        
    def stop(self):
        print("> drive move right")
        self.front_left.stop()
        self.front_right.stop()
        self.back_left.stop()
        self.back_right.stop()
        
