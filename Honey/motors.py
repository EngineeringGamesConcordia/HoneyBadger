import RPi.GPIO as GPIO
from time import sleep

class dcMotor: #for Ln298
    def __init__(self, IN1,IN2,PWM):
        self.pwm = PWM
        self.en1 = IN1
        self.en2 = IN2
        GPIO.setup(self.pwm, GPIO.OUT)
        GPIO.setup(self.en1, GPIO.OUT)
        GPIO.setup(self.en2, GPIO.OUT)
        self.pwm_speed = GPIO.PWM(self.pwm, 1000)  # 1000 Hz frequency
        self.pwm_speed.start(0)  # Start with 0% duty cycle

    def cw(self, duty_cycle):
        GPIO.output(self.en1, GPIO.LOW)
        GPIO.output(self.en2, GPIO.HIGH)
        self.pwm_speed.ChangeDutyCycle(abs(duty_cycle* 100)) # from 0 to 1

    def ccw(self, duty_cycle):
        GPIO.output(self.en1, GPIO.HIGH)
        GPIO.output(self.en2, GPIO.LOW)
        self.pwm_speed.ChangeDutyCycle(abs(duty_cycle* 100)) 

    def stop(self):
        GPIO.output(self.en1, GPIO.LOW)
        GPIO.output(self.en2, GPIO.LOW)
        self.pwm_speed.ChangeDutyCycle(0)