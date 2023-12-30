import RPi.GPIO as GPIO
from time import sleep

class dcMotor:  #for bts7960
    def __init__(self, fpwm, bpwm):
        self.fpwm = fpwm
        self.bpwm = bpwm
        GPIO.setup(self.fpwm, GPIO.OUT)
        GPIO.setup(self.bpwm, GPIO.OUT)
        self.pwm_forward = GPIO.PWM(self.fpwm, 1000)  # 1000 Hz frequency
        self.pwm_backward = GPIO.PWM(self.bpwm, 1000)
        self.pwm_forward.start(0)  # Start with 0% duty cycle
        self.pwm_backward.start(0)

    def cw(self, duty_cycle):
        self.pwm_backward.ChangeDutyCycle(0)  # Ensure backward PWM is off
        self.pwm_forward.ChangeDutyCycle(duty_cycle* 100) # from 0 to 1

    def ccw(self, duty_cycle):
        self.pwm_forward.ChangeDutyCycle(0)  # Ensure forward PWM is off
        self.pwm_backward.ChangeDutyCycle(duty_cycle* 100) 

    def stop(self):
        self.pwm_forward.ChangeDutyCycle(0)
        self.pwm_backward.ChangeDutyCycle(0)
