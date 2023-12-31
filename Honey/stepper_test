from time import sleep
import RPi.GPIO as GPIO
DIR = 19   # Direction GPIO Pin
STEP = 26  # Step GPIO Pin
CW = 1     # Clockwise Rotation
CCW = 0    # Counterclockwise Rotation
SPR = 60   # Steps per Revolution (360 / 7.5)
step_count = SPR
delay = .0108
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIR, GPIO.OUT)
GPIO.setup(STEP, GPIO.OUT)

GPIO.output(DIR, CW)
for x in range(step_count):
    #going forward
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)

GPIO.output(DIR, CCW)#move counterClockwise
for x in range(step_count):
    #going backwards
    GPIO.output(STEP, GPIO.HIGH)
    sleep(delay)
    GPIO.output(STEP, GPIO.LOW)
    sleep(delay)
GPIO.cleanup()
