import cv2
import numpy as np
from Arm_Lib import Arm_Device

# Initialize the Arm
arm = Arm_Device()

arm.Arm_serial_servo_write(1, 90, 500)
arm.Arm_serial_servo_write(2, 90, 500)
arm.Arm_serial_servo_write(3, 90, 500)
arm.Arm_serial_servo_write(4, 90, 500)
arm.Arm_serial_servo_write(5, 90, 500)
arm.Arm_serial_servo_write(6, 90, 500)