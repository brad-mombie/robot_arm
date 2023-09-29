import cv2
import numpy as np

# Initialize the video capture
cap = cv2.VideoCapture(0)

while True:
    # Capture the frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define the lower and upper range for red color
    # Note: This might need adjustment based on your environment
    lower_red = np.array([0, 100, 50])
    upper_red = np.array([30, 255, 255])


    # Create a binary mask
    mask = cv2.inRange(hsv, lower_red, upper_red)

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

    # Display the frame
    cv2.imshow('Frame', frame)

    # Press 'q' to exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
