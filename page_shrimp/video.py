from ultralytics import YOLO
import cv2

# Load YOLOv8 model
model = YOLO("runs/detect/train2/weights/best.pt")

# Load video
video_path = 0
cap = cv2.VideoCapture(video_path)

frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

# Define the codec and create VideoWriter object
#output_path = "./output.mp4"
#fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # Be sure to use the correct codec
#out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))
#print(fps)

window_width = 500  # Adjust this as needed
window_height = int(window_width * frame_height / frame_width)

frame_count = 0

ret = True
# Read frames
while ret:
    ret, frame = cap.read()
    frame_count += 1
    if frame_count % 2 == 0:
        continue
        
    if ret:
        # Detect and track objects
        results = model.track(frame, persist=True, conf=0.29)

        # Plot results on the frame
        frame_ = results[0].plot()

        # Write the frame into the file 'output.mp4'
        #out.write(frame_)

        resized_frame = cv2.resize(frame_, (window_width, window_height))

        # Visualize
        cv2.imshow("frame", resized_frame)
        if cv2.waitKey(25) & 0xFF == ord("q"):
            break

# Release everything if job is finished
cap.release()
#out.release()
cv2.destroyAllWindows()
