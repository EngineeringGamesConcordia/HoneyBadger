from math import ceil
import pcaBoard

# d-pad will go direct lines at 1/4 speed
# normal control and d-pad control will not work at the same time
CONTROLLER_SCALE = 2**15
MOTOR_SCALE = 2**16

class Drive:
    def __int__(self, pca, l_track, r_track):
        print("Init drive")
        self.pca = pca
        self.l_track = l_track
        self.r_track = r_track
        self.xL = 0x0000
        self.yL = 0x0000

    # ------------------------------ Drive stop
    def move_stop(self):
        self.pca.motorStop(self.l_track)
        self.pca.motorStop(self.r_track)

    # ------------------------------ Drive run
    def run(self):
        x = self.xL * 1.1 / CONTROLLER_SCALE  # Additional multiplier to combat imperfect strafing
        y = self.yL / CONTROLLER_SCALE
        denom = max(abs(x) + abs(y), 1)
        left_power = (y +)

    # ------------------------------ Drive front
    def move_front(self):
        print("> drive move front")
        self.left.forward()
        self.right.forward()
        self.pca.motorForward(self.l_track, abs(ceil(frontLeftPower * MOTOR_SCALE)) - 1)

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
