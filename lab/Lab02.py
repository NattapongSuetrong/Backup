import cv2
import numpy as np
from serial.tools import list_ports
import pydobot
import gtts
import os

def speak(text):
    tts = gtts.gTTS(text, lang='ja')
    tts.save('output.mp3')
    os.system('mpg321 output.mp3')

def detect_colors_and_shapes(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Define color ranges in HSV    
    red_lower = np.array([170, 50, 50])
    red_upper = np.array([180, 255, 255])

    green_lower = np.array([45,38,80])  
    green_upper = np.array([76,255,255])

    blue_lower = np.array([90, 50, 50])
    blue_upper = np.array([130, 255, 255])

    # Create masks for red, blue, and green colors
    red_mask = cv2.inRange(hsv, red_lower, red_upper)
    blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)
    green_mask = cv2.inRange(hsv, green_lower, green_upper)

    detected_color = "none"
    detected_shape = "none"
    max_area = 0

    # Find largest contour and shape
    def find_largest_contour_and_shape(mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        largest_contour = None
        max_area = 0
        shape = "none"
        for contour in contours:
            area = cv2.contourArea(contour)
            if area > max_area:
                max_area = area
                largest_contour = contour
                peri = cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, 0.04 * peri, True)
                if len(approx) == 3:
                    shape = "triangle"
                elif len(approx) == 4:
                    (x, y, w, h) = cv2.boundingRect(approx)
                    ar = w / float(h)
                    shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
                elif len(approx) > 4:
                    shape = "circle"
        return largest_contour, max_area, shape

    red_contour, red_area, red_shape = find_largest_contour_and_shape(red_mask)
    if red_contour is not None and red_area > max_area and red_area > 5000:
        detected_color = "red"
        detected_shape = red_shape
        max_area = red_area

    blue_contour, blue_area, blue_shape = find_largest_contour_and_shape(blue_mask)
    if blue_contour is not None and blue_area > max_area and blue_area > 5000:
        detected_color = "blue"
        detected_shape = blue_shape
        max_area = blue_area

    green_contour, green_area, green_shape = find_largest_contour_and_shape(green_mask)
    if green_contour is not None and green_area > max_area and green_area > 5000:
        detected_color = "green"
        detected_shape = green_shape
        max_area = green_area

    return detected_color, detected_shape
np.array([90, 50, 50])
def detect():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        detected_color, detected_shape = detect_colors_and_shapes(frame)
        print(f"Detected color: {detected_color}, Detected shape: {detected_shape}")
        if detected_color != 'none':
            break
    cap.release()
    return detected_color, detected_shape

# List available serial ports
available_ports = list_ports.comports()
print(f'Available ports: {[x.device for x in available_ports]}')

if not available_ports:
    raise Exception("No ports found")

# Select the first available port
port = available_ports[0].device

# Initialize the Dobot
device = pydobot.Dobot(port=port, verbose=False)

# Define positions
(x_home, y_home, z_home) = 259,0,130  # Home position
(x1, y1, z1) = 215,-151.8,-37.2  # Position 1
(x2, y2, z2) = 265, 58.5,-12 # Position 2

def move(point):
    device.move_to(point[0], point[1], point[2], 0, wait=True)

def main():
    z_increment = 25
    current_drop_position_z = z2  # Starting drop height
    for _ in range(3):  # Repeat the process three times
        # Move to home position
        move([x_home, y_home, z_home])
        speak("Moved to home position")
        
        # Capture an image and detect color and shape
        color, shape = detect()
        speak(f"The object is {color} and {shape} shaped.")        
        
        # Move to position 1
        move([x1, y1, 130])
        speak("Moved to position A")
        move([x1, y1, z1])
        speak("Start sucking object")
        device.suck(True)
        move([x1, y1, 130])

        # Move to drop position with updated z coordinate
        move([x2, y2, 130])
        speak("Moved to position B")
        move([x2, y2, z2])
        device.suck(False)
        speak("Stopped sucking object")

        #Move to home position
        #move([x_home, y_home, z_home])
        #speak("Moved to home position")




if __name__ == '__main__':
    main()
