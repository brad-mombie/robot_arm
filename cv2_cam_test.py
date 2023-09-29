import cv2
import numpy as np
from Arm_Lib import Arm

# Initialize the robot arm and the video capture
arm = Arm()
cap = cv2.VideoCapture(0)

# Define the threshold for adjustments and the adjustment angle for servos
threshold = 10
adjustment_angle = 5  # This is an initial value, can be adjusted based on results

while True:
    # Capture the frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper range for yellow color
    lower_yellow = np.array([20, 100, 100])
    upper_yellow = np.array([40, 255, 255])

    # Create a binary mask
    mask = cv2.inRange(hsv, lower_yellow, upper_yellow)

    # Find contours
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Find the largest contour (if any exist)
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        
        # Calculate the centroid of the largest contour
        M = cv2.moments(largest_contour)
        if M["m00"] != 0:  # avoid division by zero
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
        else:
            cx, cy = 0, 0
        
        # Draw a circle at the centroid
        cv2.circle(frame, (cx, cy), 10, (0, 255, 0), -1)

        # Get frame dimensions
        frame_center_x = frame.shape[1] // 2
        frame_center_y = frame.shape[0] // 2

        # Calculate the offset from the center
        offset_x = cx - frame_center_x
        offset_y = cy - frame_center_y

        # Adjust robot position based on the offset
        if abs(offset_x) > threshold:
            if offset_x > 0:
                # Rotate robot base to the right
                arm.Arm_serial_servo_write(1, current_angle_of_servo_1 - adjustment_angle, 500)
            else:
                # Rotate robot base to the left
                arm.Arm_serial_servo_write(1, current_angle_of_servo_1 + adjustment_angle, 500)
        
        if abs(offset_y) > threshold:
            if offset_y > 0:
                # Move robot arm down
                arm.Arm_serial_servo_write(2, current_angle_of_servo_2 - adjustment_angle, 500)
            else:
                # Move robot arm up
                arm.Arm_serial_servo_write(2, current_angle_of_servo_2 + adjustment_angle, 500)

    # Display the frame
    cv2.imshow('Frame', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
