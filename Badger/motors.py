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

    def forward(self):
        GPIO.output(self.in1, GPIO.HIGH)
        sleep(5)
        GPIO.output(self.in2, GPIO.LOW)
        sleep(1)
        GPIO.cleanup()

    def backward(self):
        GPIO.output(self.in1, GPIO.LOW)
        sleep(5)
        GPIO.output(self.in2, GPIO.HIGH)
        sleep(1)
        GPIO.cleanup()

    def stop(self):
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        GPIO.cleanup()


class servoMotor:
    GPIO.setmode(GPIO.BCM)

    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)
        GPIO.output(self.pin, True)

    # angle (int): the angle in degrees the motor should turn. between 0 an 360
    def set_angle(self, angle):
        duty = angle / 18 + 2
        pwm = GPIO.PWM(self.pin, 100)
        pwm.start(0)
        pwm.ChangeDutyCycle(duty)
        sleep(1)
        GPIO.output(self.pin, False)
        pwm.ChangeDutyCycle(0)      # set duty back to 0 -> not continuously sending inputs to servo
        GPIO.cleanup()
        
    def stop(self):
        GPIO.output(self.pin, False)
        GPIO.cleanup()


class stepperMotor:
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    # Define motor sequence
    seq = [[1,0,0,1],
            [1,0,0,0],
            [1,1,0,0],
            [0,1,0,0],
            [0,1,1,0],
            [0,0,1,0],
            [0,0,1,1],
            [0,0,0,1]]

    def __init__(self, pin1, pin2, pin3, pin4):
        self.pin1 = pin1
        self.pin2 = pin2
        self.pin3 = pin3
        self.pin4 = pin4
        GPIO.setup(self.pin1, GPIO.OUT)
        GPIO.setup(self.pin2, GPIO.OUT)
        GPIO.setup(self.pin3, GPIO.OUT)
        GPIO.setup(self.pin4, GPIO.OUT)

    # direction (str): the direction the motor should turn. 'clockwise' and 'anticlockwise'
    # angle (int): the angle in degrees the motor should turn. between 0 an 360
    def turn_stepper_motor(direction, angle):
        # Calculate steps required for given angle
        steps_per_rev = 512
        steps = int((angle/360) * steps_per_rev)

        # Set direction of motor
        if direction == 'clockwise':
            seq = seq[::-1]

        # Turn motor
        for i in range(steps):
            for halfstep in range(8):
                GPIO.output(self.pin1, seq[halfstep][0])
                GPIO.output(self.pin2, seq[halfstep][1])
                GPIO.output(self.pin3, seq[halfstep][2])
                GPIO.output(self.pin4, seq[halfstep][3])
                time.sleep(0.001)t
        
        GPIO.cleanup()