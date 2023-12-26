from math import ceil
from motors import dcMotor

# d-pad will go direct lines at 1/4 speed
# normal control and d-pad control will not work at the same time
CONTROLLER_SCALE = 2**15
MOTOR_SCALE = 2**16

class Drive:
    def __int__(self, l_track, r_track):
        print("Init drive")
        self.l_track = l_track
        self.r_track = r_track

    # ------------------------------ Drive stop
    def move_stop(self):
        print("> vacuum start")
        self.l_track.stop()
        self.r_track.stop()

    # ------------------------------ Drive front
    def move_front(self):
        print("> drive move front")
        self.l_track.cw()
        self.r_track.ccw()

    # ------------------------------ Drive back
    def move_back(self):
        print("> drive move back")
        self.l_track.ccw()
        self.r_track.cw()

    # ------------------------------ Drive left
    def move_left(self):
        print("> drive move left")
        self.l_track.cw()
        self.r_track.cw()

    # ------------------------------ Drive right
    def move_right(self):
        print("> drive move right")
        self.l_track.ccw()
        self.r_track.ccw()
