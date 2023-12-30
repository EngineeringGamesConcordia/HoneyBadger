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

        #code below to get rid of
class stepperMotor:
    def __init__(self, dir, step, speed): #should be 19, 26,.0108
        self.dir = dir
        self.step = step
        self.delay = speed #.0208 #speed
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.dir, GPIO.OUT)
        GPIO.setup(self.step, GPIO.OUT)
    def cw(self):
        #could have a small for loop which will make it do a few movement
        GPIO.output(self.dir, GPIO.HIGH)
        GPIO.output(self.step, GPIO.HIGH)
        sleep(self.delay)
        GPIO.output(self.step, GPIO.LOW)
        sleep(self.delay)
        
    def ccw(self):
        GPIO.output(self.dir, GPIO.LOW)
        GPIO.output(self.step, GPIO.HIGH)
        sleep(self.delay)
        GPIO.output(self.step, GPIO.LOW)
        sleep(self.delay)
    #no need for stop function has works by step
        