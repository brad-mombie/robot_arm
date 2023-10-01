import cv2
import numpy as np

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
        
        # Draw the bounding rectangle around the contour
        cv2.rectangle(frame, (x, y), (x+w, y+h), (1, 227, 254), 2)

    # Display the frame
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the camera and close the window
cap.release()
cv2.destroyAllWindows()
