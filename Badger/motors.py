import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BOARD)
class dcMotor:
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