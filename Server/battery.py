from led import Led
from adc import ADC

import logging
import math
import time

BATTERY_COLOR = [0, 50, 0]    # not super bright green
USEFUL_VOLTAGE_FLOOR = 6       # below 4 volts the batteries can't do much, so don't need to track that part of the range

def main():
 
    print("Starting battery checker ...")
    led_controller = Led()
    #led_controller.first_test()

    adc_controller = ADC()
    servo_voltage = adc_controller.read_battery_voltage_servo()
    control_voltage = adc_controller.read_battery_voltage_controller()

    print("Servo voltage:    ", servo_voltage)
    print("Control voltage:  ", control_voltage)

    servo_voltage_rounded = int(math.floor(servo_voltage))
    control_voltage_rounded = int(math.floor(control_voltage))

    print("Servo voltage:    ", servo_voltage_rounded)
    print("Control voltage:  ", control_voltage_rounded)

    led_controller.color_wipe_to(BATTERY_COLOR, servo_voltage_rounded - USEFUL_VOLTAGE_FLOOR)
    time.sleep(3)
    led_controller.turn_off()

    time.sleep(1)

    led_controller.color_wipe_to(BATTERY_COLOR, control_voltage_rounded - USEFUL_VOLTAGE_FLOOR)
    time.sleep(3)
    led_controller.turn_off()
    
    print("Complete!")

if __name__ == "__main__":
    main()
