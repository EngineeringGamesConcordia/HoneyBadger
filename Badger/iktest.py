import tinyik
import numpy as np

arm = tinyik.Actuator(['z', [1., 0., 0.], 'z', [1., 0., 0.]])

arm.ee = [2 / np.sqrt(2), 2 / np.sqrt(2), 0.]
arm.angles
print(np.round(np.rad2deg(arm.angles)))

