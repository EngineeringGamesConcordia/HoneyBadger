from motors import dcMotor
from math import ceil

class Drive:
    def __init__(self, front_left, front_right, back_left, back_right):
        print("Init drive")
        self.front_left = front_left
        self.front_right = front_right
        self.back_left = back_left
        self.back_right = back_right
        self.front_left_speed = 0
        self.front_right_speed = 0
        self.back_left_speed = 0
        self.back_right_speed = 0
        self.angular_rot =0
        self.wheel_radius = 0.04 #80mm wheel
        self.honey_geometry = (0.255+0.23) #25.5cm lenght and 23cm wide
    
    def convert(self,speed,speedy):
        self.x = (speed/2**15) # scaling them to 0-1
        self.y = (speed/2**15)
        self.front_left_speed = ((self.x - self.y) - ((self.honey_geometry)*self.angular_rot))/self.wheel_radius
        self.front_right_speed = ((self.x + self.y) + ((self.honey_geometry)*self.angular_rot))/self.wheel_radius
        self.back_left_speed = ((self.x - self.y) - ((self.honey_geometry)*self.angular_rot))/self.wheel_radius
        self.back_right_speed = ((self.x + self.y) + ((self.honey_geometry)*self.angular_rot))/self.wheel_radius
        print("Speeds fl: " + str(self.front_left_speed) +" bl: " + str(self.back_left_speed) +"fr: " + str(self.front_right_speed) +"br: " + str(self.back_right_speed))
    # ------------------------------ Drive front
    def move_front(self,speed):
        self.speed = (speed/2**15)
        print("> drive move front")
        self.front_left.cw(self.speed)
        self.front_right.ccw(self.speed)
        self.back_left.cw(self.speed)
        self.back_right.ccw(self.speed)

    # ------------------------------ Drive back
    def move_back(self,speed):
        self.speed = (speed/2**15)
        print("> drive move back")
        self.front_left.ccw(self.speed)
        self.front_right.cw(self.speed)
        self.back_left.ccw(self.speed)
        self.back_right.cw(self.speed)
        
    # ------------------------------ Drive left
    def move_left(self,speed):
        self.speed = (speed/2**15)
        print("> drive move left")
        self.front_left.cw(self.speed)
        self.front_right.ccw(self.speed)
        self.back_left.ccw(self.speed)
        self.back_right.cw(self.speed)

    # ------------------------------ Drive right
    def move_right(self,speed):
        self.speed = (speed/2**15)
        print("> drive move right")
        self.front_left.cw(self.speed)
        self.front_right.ccw(self.speed)
        self.back_left.cw(self.speed)
        self.back_right.ccw(self.speed)
        
    def turn_left(self):
        self.speed = 1
        print("> drive turn left")
        self.front_left.cw(self.speed)
        self.front_right.cw(self.speed)
        self.back_left.cw(self.speed)
        self.back_right.cw(self.speed)
        
    def turn_right(self):
        self.speed = 1
        print("> drive turn right")
        self.front_left.ccw(self.speed)
        self.front_right.ccw(self.speed)
        self.back_left.ccw(self.speed)
        self.back_right.ccw(self.speed)
        
    def stop(self):
        self.front_left.stop()
        self.front_right.stop()
        self.back_left.stop()
        self.back_right.stop()
        
