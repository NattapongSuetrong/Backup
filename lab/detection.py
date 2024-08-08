import cv2
import numpy as np

# Define the color ranges in HSV
red_lower = np.array([170, 50, 50])
red_upper = np.array([180, 255, 255])

green_lower = np.array([45,38,80])
green_upper = np.array([76,255,255])

blue_lower = np.array([90, 50, 50])
blue_upper = np.array([130, 255, 255])

# Start the webcam
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to HSV color space
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Create masks for red and blue colors
    red_mask = cv2.inRange(hsv, red_lower, red_upper)
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
    green_mask = cv2.inRange(hsv, green_lower, green_upper)

    # Find contours for the red mask
    contours, _ = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    max_red_area = 0
    max_red_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_red_area:
            max_red_area = area
            max_red_contour = contour

    if max_red_contour is not None and max_red_area > 5000:
        (x, y), radius = cv2.minEnclosingCircle(max_red_contour)
        center = (int(x), int(y))
        radius = int(radius)
        if radius > 10:
            cv2.circle(frame, center, radius, (0, 0, 255), 2)
            cv2.putText(frame, 'Red', (center[0] - 20, center[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # Find contours for the blue mask
    contours, _ = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    max_blue_area = 0
    max_blue_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_blue_area:
            max_blue_area = area
            max_blue_contour = contour

    if max_blue_contour is not None and max_blue_area > 5000:
        (x, y), radius = cv2.minEnclosingCircle(max_blue_contour)
        center = (int(x), int(y))
        radius = int(radius)
        if radius > 10:
            cv2.circle(frame, center, radius, (255, 0, 0), 2)
            cv2.putText(frame, 'Blue', (center[0] - 20, center[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2)

    # Find contours for the green mask
    contours, _ = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    max_green_area = 0
    max_green_contour = None
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > max_green_area:
            max_green_area = area
            max_green_contour = contour

    if max_green_contour is not None and max_green_area > 5000:
        (x, y), radius = cv2.minEnclosingCircle(max_green_contour)
        center = (int(x), int(y))
        radius = int(radius)
        if radius > 10:
            cv2.circle(frame, center, radius, (0, 255, 0), 2)
            cv2.putText(frame, 'green', (center[0] - 20, center[1] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
    
    
    # Display the frame
    cv2.imshow('Frame', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the webcam and close all windows
cap.release()
cv2.destroyAllWindows()
