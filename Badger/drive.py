from math import ceil
from motors import dcMotor

# d-pad will go direct lines at 1/4 speed
# normal control and d-pad control will not work at the same time
CONTROLLER_SCALE = 2**15
MOTOR_SCALE = 2**16

class Drive:
    def __init__(self, l_track, r_track):
        print("Init drive")
        self.l_track = l_track
        self.r_track = r_track

    # ------------------------------ Drive stop
    def move_stop(self):
        #print("> dc stop")
        self.l_track.stop()
        self.r_track.stop()

    # ------------------------------ Drive front
    def move_front(self,speed):
        print("> drive move front at" +str(speed))
        self.l_track.ccw(speed)
        self.r_track.cw(speed)

    # ------------------------------ Drive back
    def move_back(self,speed):
        print("> drive move back at"+str(speed))
        self.l_track.cw(speed)
        self.r_track.ccw(speed)

    # ------------------------------ Drive left
    def move_left(self,speed):
        print("> drive move left at"+str(speed))
        self.l_track.ccw(speed)
        self.r_track.ccw(speed)

    # ------------------------------ Drive right
    def move_right(self,speed):
        self.speed = speed
        print("> drive move right at"+str(speed))
        self.l_track.cw(speed)
        self.r_track.cw(speed)
