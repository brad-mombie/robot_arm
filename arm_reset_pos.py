import cv2
import numpy as np
from Arm_Lib import Arm_Device

# Initialize the Arm
arm = Arm_Device()

while True:
    print("servo_1: ", arm.Arm_serial_servo_read(1))
    print("servo_2: ", arm.Arm_serial_servo_read(2))
    print("servo_3: ", arm.Arm_serial_servo_read(3))
    print("servo_4: ", arm.Arm_serial_servo_read(4))
    print("servo_5: ", arm.Arm_serial_servo_read(5))
    print("servo_6: ", arm.Arm_serial_servo_read(6))