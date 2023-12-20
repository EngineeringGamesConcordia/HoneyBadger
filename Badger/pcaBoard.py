from board import SCL, SDA
import busio
from adafruit_pca9685 import PCA9685
from adafruit_motor import servo
from time import sleep
import RPi.GPIO as GPIO

DEFAULT_SCALE_FACTOR = 1 / (2 ** 12)


class mServo:
    def __init__(self, pin, initAngle=0, minAngle=0, maxAngle=270):
        print("initializing new servo on pin " + str(pin) + " init: " + str(initAngle) + " min: " + str(
            minAngle) + " max: " + str(maxAngle))
        self.minAngle = minAngle
        self.maxAngle = maxAngle
        self.pin = pin
        self.increment = 0  # Raw value from joy stick, needs to be scaled by self.scale
        self.servo = None
        self.scale = DEFAULT_SCALE_FACTOR

    def setScale(self, val):
        self.scale = val

    def setAngle(self, angle):
        print("PCA setAngle, servo: " + str(self.pin) + " angle: " + str(angle))
        if (self.minAngle <= angle <= self.maxAngle):
            self.servo.angle = angle
        else:
            print("Angle " + str(angle) + " illegal")

    def setIncrement(self, val):
        self.increment = val

    def step(self):
        temp = self.servo.angle + (self.increment * self.scale)
        if (self.minAngle <= temp <= self.maxAngle):
            if (abs(temp - self.servo.angle) <= 1):
                print("Servo " + str(self.pin) + " angle: " + str(self.servo.angle))
            self.servo.angle = temp


# speed is value from [0x0000..0xFFFF]
class mMotor:
    def __init__(self, in1, in2, pwmPin):
        print("Adding motor with in1: " + str(in1) + ", in2: " + str(in2) + ", pwm: " + str(pwmPin))
        self.in1 = in1
        self.in2 = in2
        self.pwmPin = pwmPin
        self.speed = 0x0000
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)

    def forward(self, val):
        print("PCA forward, motor: " + str(self.pwmPin) + " speed: " + str(val))
        if (0x0000 <= val <= 0xFFFF):
            GPIO.output(self.in1, GPIO.HIGH)
            GPIO.output(self.in2, GPIO.LOW)
            self.speed = val
        else:
            print("val " + str(val) + " illegal")

    def reverse(self, val):
        print("PCA reverse, motor: " + str(self.pwmPin) + " speed: " + str(val))
        if (0x0000 <= val <= 0xFFFF):
            GPIO.output(self.in1, GPIO.LOW)
            GPIO.output(self.in2, GPIO.HIGH)
            self.speed = val
        else:
            print("val " + str(val) + " illegal")

    def stop(self):
        # print("PCA stop, motor: "+str(self.pwmPin))
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.HIGH)
        self.speed = 0xFFFF

    def neutral(self):
        # print("PCA neutral, motor: "+str(self.pwmPin))
        GPIO.output(self.in1, GPIO.HIGH)
        GPIO.output(self.in2, GPIO.HIGH)
        self.speed = 0x0000


# Assuming Servos are always attached in order from 0..15 and motors from 15..0
class PcaBoard:
    def __init__(self, address=64):
        print("PCA board init, address:" + str(address))
        self.i2c_bus = busio.I2C(SCL, SDA)
        self.pca = PCA9685(self.i2c_bus, address=address)
        self.pca.frequency = 50
        self.servos = []
        self.motors = []

    def addServo(self, initAngle=0, minAngle=0, maxAngle=270):
        if len(self.servos) < 16:
            i = len(self.servos)
            self.servos.append(mServo(i, initAngle=initAngle, minAngle=minAngle, maxAngle=maxAngle))
            self.servos[i].servo = servo.Servo(self.pca.channels[i], min_pulse=500, max_pulse=2500, actuation_range=270)
            self.servos[i].servo.angle = initAngle
            return i
        else:
            print("Already at max servos")
            return None

    def addMotor(self, in1, in2):
        if len(self.servos) + len(self.motors) < 16:
            i = 15 - len(self.motors)
            self.motors.append(mMotor(in1, in2, i))
            return i
        else:
            print("Already at max servos + motors")
            return None

    def setAngle(self, servo, angle):
        if (servo < len(self.servos)):
            self.servos[servo].setAngle(angle)
            print("setting servo " + str(servo) + " to " + angle)
        else:
            print("Servo " + str(servo) + "out of index")

    def setServoIncrement(self, servo, val):
        if (servo < len(self.servos)):
            self.servos[servo].setIncrement(val)
        else:
            print("Servo " + str(servo) + "out of index")

    def setServoScale(self, servo, val):
        if (servo < len(self.servos)):
            self.servos[servo].setScale(val)
        else:
            print("Servo " + str(servo) + "out of index")

    def motorForward(self, motor, val):
        if (motor >= 15 - len(self.motors)):
            self.motors[15 - motor].forward(val)
        else:
            print("Motor " + str(motor) + "out of index")

    def motorReverse(self, motor, val):
        if (motor >= 15 - len(self.motors)):
            self.motors[15 - motor].reverse(val)
        else:
            print("Motor " + str(motor) + "out of index")

    def motorStop(self, motor):
        if (motor >= 15 - len(self.motors)):
            self.motors[15 - motor].stop()
        else:
            print("Motor " + str(motor) + "out of index")

    def motorNeutral(self, motor):
        if (motor >= 15 - len(self.motors)):
            self.motors[15 - motor].neutral()
        else:
            print("Motor " + str(motor) + "out of index")

    # Duty Cycle range [0x0000, 0xFFFF] = [0, 65535] for 0% to 100%
    def setDutyCycle(self, pin, amount):
        print("PCA setDutyCycle, pin: " + str(pin) + " amount: " + str(amount))
        if (0x0000 <= amount <= 0xFFFF):
            self.pca.channels[pin].duty_cycle = amount
        else:
            print("Amount " + str(amount) + " illegal")

    def step(self):
        for s in self.servos:
            s.step()
        for m in self.motors:
            self.pca.channels[m.pwmPin].duty_cycle = m.speed