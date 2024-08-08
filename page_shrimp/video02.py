import cv2
from sort import *
import math
import numpy as np
from ultralytics import YOLO
import cvzone
import torch
import time
from fastapi import WebSocket, WebSocketDisconnect

video2_running = False
video_value = [0, 10]
clients = []
counter = []

cap = cv2.VideoCapture(0)

def start():
    model = YOLO("runs/detect/train2/weights/best.pt")

    classname = {0: "shrimp"}

    trackers = Sort(max_age=20)

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    

    line = [0, 240, 640, 240]
    
    
    frame_count = 0
    
    global video2_running, video_value, counter
    video2_running = True
    #fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # codec for mp4 format
    #out = cv2.VideoWriter("output.mp4", fourcc, 20.0, (frame_width, frame_height))

    while video2_running:
        ret, frame = cap.read()
        #if not ret:
            #cap = cv2.videocapture("test_Trim.mp4")
            #continue
            
        frame_count += 1
        if frame_count % 2 == 0:
            continue
            
        #frame = cv2.resize(frame, (320, 240))  # Lower resolution

        detections = np.empty((0, 5), int)
        results = model(frame, stream=1)
        for info in results:
            boxes = info.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]
            conf = box.conf[0]
            classindex = box.cls[0]

            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            conf = math.ceil(conf * 100)
            classindex = int(classindex)
            new_detection = np.array([x1, y1, x2, y2, conf])
            detections = np.vstack((detections, new_detection))

        track_result = trackers.update(detections)
        cv2.line(frame, (line[0], line[1]), (line[2], line[3]), (0, 255, 255), 2)
        for results in track_result:
            x1, y1, x2, y2, track_id = results
            x1, y1, x2, y2, track_id = int(x1), int(y1), int(x2), int(y2), int(track_id)
            w, h = x2 - x1, y2 - y1
            cx, cy = x1 + w // 2, y1 + h // 2

            cv2.circle(frame, (cx, cy), 6, (0, 0, 255), -1)
            #cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
            if line[0] - 20 < cx < line[2] + 20 and line[1] < cy < line[3]:
                cv2.line(frame, (line[0], line[1]), (line[2], line[3]), (255, 0, 0), 2)
                if counter.count(track_id) == 0:
                    counter.append(track_id)

        cvzone.putTextRect(
            frame,
            f"Counter: {len(counter)}",
            [10, 50],
            thickness=2,
            scale=2,
        )
        
    
        #notify_clients()
        print(f"Video is running: {len(counter)}")

        
        cv2.imshow("frame", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    cap.release()
    cv2.destroyAllWindows()
        
def stop():
    global video2_running
    video2_running = False
    print("Video stopped")
    
def notify_clients():
    global clients, video_value
    for client in clients:
        print('in')
        try:
            client.send_text(f"Value changed: {video_value}")
            print(f"Sent to client: Value changed: {video_value}")  # เพิ่มการพิมพ์ข้อความที่ส่งไปยัง clients
        except WebSocketDisconnect:
            clients.remove(client)
            print("Client disconnected and removed")  # เพิ่มการพิมพ์เมื่อ client ถูกถอดออก

if __name__ == "__main__":
    start()
