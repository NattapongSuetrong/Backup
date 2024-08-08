import cv2

def main():
    # Open the video camera (the default camera connected or the first camera)
    cap = cv2.VideoCapture(0)

    # Check if the camera was opened correctly
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Loop to capture frames continuously
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()

        # Display the frame
        cv2.imshow('Camera', frame)

        # Exit loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release the camera and close all OpenCV windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
