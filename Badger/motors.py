import RPi.GPIO as GPIO
from time import sleep

class dcMotor:
    GPIO.setmode(GPIO.BOARD)
    def __init__(self, in1, in2, pwmPin):
        self.in1 = in1
        self.in2 = in2
        self.pwmPin = pwmPin
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.pwmPin, GPIO.OUT)

    def forward(self, speed):
        GPIO.output(self.in1, GPIO.HIGH)
        sleep(5)
        GPIO.output(self.in2, GPIO.LOW)
        sleep(1)
        pwm = GPIO.PWM(self.pwmPin, 100)
        pwm.start(speed)
        GPIO.output(self.pwmPin, GPIO.HIGH)

    def backward(self, speed):
        GPIO.output(self.in1, GPIO.LOW)
        sleep(5)
        GPIO.output(self.in2, GPIO.HIGH)
        sleep(1)
        pwm = GPIO.PWM(self.pwmPin, 100)
        pwm.start(speed)
        GPIO.output(self.pwmPin, GPIO.HIGH)

    def stop(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)


class servoMotor:
    GPIO.setmode(GPIO.BCM)
    frequency = 330
    neutral_duty_cycle = 60

    def __init__(self, pin, initAngle = 0, minAngle=0, maxAngle=270):
        self.pin = pin
        self.minAngle = minAngle
        self.maxAngle = maxAngle
        GPIO.setup(self.pin, GPIO.OUT)

    def set_angle(self, angle):
        duty = angle / 18 + 2
        GPIO.output(self.pin, True)
        pwm = GPIO.PWM(self.pin, 100)
        pwm.start(0)
        pwm.ChangeDutyCycle(duty)
        sleep(1)
        GPIO.output(self.pin, False)
        pwm.ChangeDutyCycle(0)      # set duty back to 0 -> not continuously sending inputs to servo
