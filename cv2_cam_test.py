import cv2
import numpy as np
from Arm_Lib import Arm_Device

# Initialize the Arm
arm = Arm_Device()

# Initialize the current angles of the servos
current_angle_of_servo_1 = arm.Arm_serial_servo_read(1) or 90  
current_angle_of_servo_2 = arm.Arm_serial_servo_read(2) or 90  
current_angle_of_servo_3 = arm.Arm_serial_servo_read(3) or 90  

# Define deadband values
deadband_horizontal = 20
deadband_vertical = 20

# Max area threshold
max_area_threshold = 44370

# Start capturing video from the first camera device
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    
    # Apply Gaussian blur to the frame
    blurred_frame = cv2.GaussianBlur(frame, (15, 15), 0)
    
    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

    # Define the HSV range for green
    lower_green = np.array([30, 40, 40])
    upper_green = np.array([90, 255, 255])

    # Create a binary mask where the green range is white
    mask = cv2.inRange(hsv, lower_green, upper_green)


    # Find contours in the frame
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        c = max(contours, key=cv2.contourArea)
        
        # Get the bounding rectangle of the contour
        x, y, w, h = cv2.boundingRect(c)
        
        # Check if the bounding box area exceeds the threshold
        if w * h > max_area_threshold:
            # Move the arm to the neutral position
            arm.Arm_serial_servo_write(1, 92, 500)
            arm.Arm_serial_servo_write(2, 114, 500)
            arm.Arm_serial_servo_write(3, 26, 500)
            arm.Arm_serial_servo_write(4, 29, 500)
            arm.Arm_serial_servo_write(5, 89, 500)
            continue  # Skip the rest of the loop and start a new frame

    

        # Logic to move the arm
        adjustment_angle = 2

        # Horizontal tracking
        if cx < 290 - deadband_horizontal:
            if current_angle_of_servo_1 < 180:
                current_angle_of_servo_1 += adjustment_angle
                arm.Arm_serial_servo_write(1, current_angle_of_servo_1, 500)
        elif cx > 350 + deadband_horizontal:
            if current_angle_of_servo_1 > 0:
                current_angle_of_servo_1 -= adjustment_angle
                arm.Arm_serial_servo_write(1, current_angle_of_servo_1, 500)

        # Vertical tracking using two servos
        if cy < 210 - deadband_vertical:
            if current_angle_of_servo_2 < 180:
                current_angle_of_servo_2 += adjustment_angle
                arm.Arm_serial_servo_write(2, current_angle_of_servo_2, 500)
            if current_angle_of_servo_3 < 180:
                current_angle_of_servo_3 += adjustment_angle
                arm.Arm_serial_servo_write(3, current_angle_of_servo_3, 500)
        elif cy > 270 + deadband_vertical:
            if current_angle_of_servo_2 > 0:
                current_angle_of_servo_2 -= adjustment_angle
                arm.Arm_serial_servo_write(2, current_angle_of_servo_2, 500)
            if current_angle_of_servo_3 > 0:
                current_angle_of_servo_3 -= adjustment_angle
                arm.Arm_serial_servo_write(3, current_angle_of_servo_3, 500)


    # Display the frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
