# coding:utf-8
from pca9685 import PCA9685
import time

PWM_RELAX = 4096

def map_value(value, from_low, from_high, to_low, to_high):
    """Map a value from one range to another."""
    return (to_high - to_low) * (value - from_low) / (from_high - from_low) + to_low

class Servo:
    def __init__(self):
        self.pwm_40 = PCA9685(0x40, debug=True)
        self.pwm_41 = PCA9685(0x41, debug=True)
        # Set the cycle frequency of PWM to 50 Hz
        self.pwm_40.set_pwm_freq(50)
        time.sleep(0.01)
        self.pwm_41.set_pwm_freq(50)
        time.sleep(0.01)

    def set_servo_angle(self, channel, angle):
        """
        Set the servo angle on a PCA9685 module.
        
        :param channel: Servo channel (0-31)
        :param angle: Angle in degrees (0-180)
        """
        # Servo pulse range in microseconds
        SERVO_MIN_US = 500   # 0 degrees
        SERVO_MAX_US = 2500  # 180 degrees
        PWM_PERIOD_US = 20000  # 20 ms period (50 Hz)
        MAX_COUNT = 4095       # 12-bit PCA9685

        # Convert angle to pulse width in µs
        pulse_us = SERVO_MIN_US + (angle / 180.0) * (SERVO_MAX_US - SERVO_MIN_US)
        
        # Convert pulse width to PCA9685 register value
        duty_count = int(pulse_us / PWM_PERIOD_US * MAX_COUNT)

        # Select the correct board/module
        if channel < 16:
            self.pwm_41.set_pwm(channel, 0, duty_count)
        elif 16 <= channel < 32:
            sub_channel = channel - 16
            self.pwm_40.set_pwm(sub_channel, 0, duty_count)
        else:
            raise ValueError("Error: invalid channel, channel must be between 0 and 32")


    def relax(self):
        """Relax all servos by setting their PWM values to 4096."""
        for i in range(8):
            self.pwm_41.set_pwm(i + 8, PWM_RELAX, PWM_RELAX)
            self.pwm_40.set_pwm(i, PWM_RELAX, PWM_RELAX)
            self.pwm_40.set_pwm(i + 8, PWM_RELAX, PWM_RELAX)

RIGHT_KNEES = [10, 13, 31]
LEFT_KNEES = [18, 21, 27]

RIGHT_KNEE_START_ANGLE = 10
LEFT_KNEE_START_ANGLE = 170
DEFAULT_START_ANGLE = 90

# Main program logic follows:
if __name__ == '__main__':
    print("Now servos will rotate to certain angles.")
    print("Please keep the program running when installing the servos.")
    print("After that, you can press ctrl-C to end the program.")
    servo = Servo()
    while True:
        try:
            for i in range(32):
                print(f"Setting servo: {i}")
                if i in RIGHT_KNEES:
                    servo.set_servo_angle(i, RIGHT_KNEE_START_ANGLE)
                elif i in LEFT_KNEES:
                    servo.set_servo_angle(i, LEFT_KNEE_START_ANGLE)
                else:
                    servo.set_servo_angle(i, DEFAULT_START_ANGLE)
            time.sleep(3)
        except KeyboardInterrupt:
            print("\nEnd of program")
            servo.relax()
            break
