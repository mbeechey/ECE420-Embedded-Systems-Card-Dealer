import RPi.GPIO as GPIO
import time
import random

# Motor 1 pins
IN1 = 25
IN2 = 26

# Motor 2 pins
IN3 = 19
IN4 = 13

pwm_motor1 = None
pwm_motor2 = None

def setup():
    global pwm_motor1, pwm_motor2
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(IN1, GPIO.OUT)
    GPIO.setup(IN2, GPIO.OUT)
    GPIO.setup(IN3, GPIO.OUT)
    GPIO.setup(IN4, GPIO.OUT)
    
    # Initialize PWM on IN1 and IN3 with 1kHz frequency
    pwm_motor1 = GPIO.PWM(IN1, 1000)
    pwm_motor2 = GPIO.PWM(IN3, 1000)
    
    # Start with 0% duty cycle (stopped)
    pwm_motor1.start(0)
    pwm_motor2.start(0)
    
    # Keep IN2 and IN4 LOW for forward motion
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

def motor1_forward(speed=50): # 50% speed by default
    GPIO.output(IN2, GPIO.LOW)
    pwm_motor1.ChangeDutyCycle(speed)

def motor1_stop():
    if pwm_motor1:
        pwm_motor1.ChangeDutyCycle(0)

def motor2_forward(speed=50):
    GPIO.output(IN4, GPIO.LOW)
    pwm_motor2.ChangeDutyCycle(speed)

def motor2_stop():
    if pwm_motor2:
        pwm_motor2.ChangeDutyCycle(0)

def stop_all():
    motor1_stop()
    motor2_stop()

def shuffle(duration=5.0):
    start_time = time.time()
    print(f"Starting shuffle for {duration} seconds...")
    
    while time.time() - start_time < duration:
        # Randomly choose which motor to run: 1, 2, or both (3)
        choice = random.choice([1, 2, 3])
        
        # Run for a short random duration (e.g., 50ms to 200ms) to drop a few cards at a time
        run_time = random.uniform(0.05, 0.2) 
        
        if choice == 1:
            motor1_forward()
            motor2_stop()
        elif choice == 2:
            motor1_stop()
            motor2_forward()
        else:
            motor1_forward()
            motor2_forward()
            
        time.sleep(run_time)
        
    stop_all()
    print("Shuffle complete.")

def cleanup():
    stop_all()
    if pwm_motor1:
        pwm_motor1.stop()
    if pwm_motor2:
        pwm_motor2.stop()
    GPIO.cleanup()

if __name__ == "__main__":
    try:
        setup()
        shuffle(5.0)
    except KeyboardInterrupt:
        print("\nInterrupted")
    finally:
        cleanup()
