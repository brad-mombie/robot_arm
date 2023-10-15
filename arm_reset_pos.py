import cv2
import time
import numpy as np
from Arm_Lib import Arm_Device

# Initialize the Arm
arm = Arm_Device()


print("servo_1: ", arm.Arm_serial_servo_read(1))
print("servo_2: ", arm.Arm_serial_servo_read(2))
print("servo_3: ", arm.Arm_serial_servo_read(3))
print("servo_4: ", arm.Arm_serial_servo_read(4))
print("servo_5: ", arm.Arm_serial_servo_read(5))
print("servo_6: ", arm.Arm_serial_servo_read(6))

arm.Arm_serial_servo_write(1, 40, 500)
time.sleep(1)
arm.Arm_serial_servo_write(2, 114, 500)
time.sleep(1)
arm.Arm_serial_servo_write(3, 26, 500)
time.sleep(1)
arm.Arm_serial_servo_write(4, 29, 500)
time.sleep(1)
arm.Arm_serial_servo_write(5, 89, 500)
time.sleep(1)

