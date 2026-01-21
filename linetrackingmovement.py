from machine import Pin, PWM
import time

# === Digital IR Sensors ===
left_sensor = Pin(27, Pin.IN)   # left IR
right_sensor = Pin(26, Pin.IN)  # right IR

class Motor:
    def __init__(self, speed_pin, in1_pin, in2_pin):
        self.in1 = Pin(in1_pin, Pin.OUT)
        self.in2 = Pin(in2_pin, Pin.OUT)
        self.pwm = PWM(Pin(speed_pin))
        self.pwm.freq(1000)

    def forward(self, speed=512):
        self.in1.value(1)
        self.in2.value(0)
        self.set_speed(speed)

    def backward(self, speed=512):
        self.in1.value(0)
        self.in2.value(1)
        self.set_speed(speed)

    def stop(self):
        self.in1.value(0)
        self.in2.value(0)
        self.set_speed(0)

    def set_speed(self, speed):
        self.pwm.duty_u16(min(max(speed, 0), 65535))


class Car:
    def __init__(self, m1, m2, m3, m4, ftime, btime, stime, car_speed):
        self.m1 = m1
        self.m2 = m2
        self.m3 = m3
        self.m4 = m4
        self.ftime = ftime
        self.btime = btime
        self.stime = stime
        self.car_speed = car_speed

    def move_forward(self):
        print("Moving Forward 🚗💨")
        self.m1.forward(self.car_speed)
        self.m2.forward(self.car_speed)
        self.m3.forward(self.car_speed)
        self.m4.forward(self.car_speed)
        time.sleep(self.ftime)

    def move_backward(self):
        print("Reversing... ⏪")
        self.m1.backward(self.car_speed)
        self.m2.backward(self.car_speed)
        self.m3.backward(self.car_speed)
        self.m4.backward(self.car_speed)
        time.sleep(self.btime)

    def stop_motors(self):
        print("Stopping ⛔")
        self.m1.stop()
        self.m2.stop()
        self.m3.stop()
        self.m4.stop()
        time.sleep(self.stime)

    # === Add simple turn methods to Car for line-following ===
    def turn_left(self):
        print("Turning Left ⬅️")
        self.m1.stop()
        self.m2.stop()
        self.m3.forward(self.car_speed)
        self.m4.forward(self.car_speed)
    
    def turn_right(self):
        print("Turning Right ➡️")
        self.m1.forward(self.car_speed)
        self.m2.forward(self.car_speed)
        self.m3.stop()
        self.m4.stop()
    
    # === Line-following loop ===
    def line_follow(self):
        print("Starting line-follow mode... (Press Ctrl+C to stop)")
        while True:
            left_val = left_sensor.value()
            right_val = right_sensor.value()
    
            # Print sensor values for debugging
            print("Left:", left_val, " | Right:", right_val)
    
            # Adjust logic if your sensor reads 1 for black and 0 for white
            left_on_line = left_val == 1
            right_on_line = right_val == 1
    
            if left_on_line and right_on_line:
                self.forward()
            elif left_on_line and not right_on_line:
                self.turn_left()
            elif not left_on_line and right_on_line:
                self.turn_right()
            else:
                self.stop_motors()
    
            time.sleep(0.05)  # small delay for stability

# === Run line-following test ===

# === Motor Pin Mapping ===
motor_A = Motor(10, 11, 12)  # Back Left
motor_B = Motor(13, 14, 15)  # Front Left
motor_C = Motor(20, 16, 17)  # Front Right
motor_D = Motor(21, 19, 18)  # Back Right

# === Instantiate Car ===
forward_time = 3
backward_time = 2
stop_time = 1
yellow_car = Car(motor_A, motor_B, motor_C, motor_D, forward_time, backward_time, stop_time, car_speed=30000)

# === Demo ===
def demo():
    yellow_car.line_follow()

demo()


