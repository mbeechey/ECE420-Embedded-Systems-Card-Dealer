import RPi.GPIO as GPIO
import time

SERVO_PIN = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(SERVO_PIN, GPIO.OUT)

pwm = GPIO.PWM(SERVO_PIN, 50)
pwm.start(0)

# MG90S servos often have a tighter pulse width range for 180 degrees
# Try 2.0 to 10.0 or 2.0 to 12.0. If it still goes too far, 2.5 to 10.0 might be best.
MIN_DUTY = 2.0
MAX_DUTY = 11.0

# 0.02 was too fast and caused overshoot. 0.05 is a good middle ground
speed_delay = 0.13
strength_hold = False

last_duty = None

def angle_to_duty(angle):
    return MIN_DUTY + (angle / 180.0) * (MAX_DUTY - MIN_DUTY)

def set_duty_smooth(duty):
    global last_duty
    if last_duty is None or abs(duty - last_duty) > 0.05:
        pwm.ChangeDutyCycle(duty)
        last_duty = duty

def move_slow(start, end):
    step = 2 if end > start else -2
    for angle in range(start, end + step, step):
        set_duty_smooth(angle_to_duty(angle))
        time.sleep(speed_delay)

    time.sleep(0.5)

    if not strength_hold:
        pwm.ChangeDutyCycle(0)

try:
    move_slow(90, 180)
    time.sleep(5)
    move_slow(180, 90)
    time.sleep(2)

finally:
    pwm.ChangeDutyCycle(angle_to_duty(90))
    time.sleep(1)
    pwm.ChangeDutyCycle(0)
    pwm.stop()
    GPIO.cleanup()



