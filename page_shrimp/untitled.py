import cv2

# เปิดการเชื่อมต่อกับกล้อง (ค่า 0 หมายถึงกล้องตัวแรก)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("ไม่สามารถเปิดกล้องได้")
    exit()

while True:
    # อ่านภาพจากกล้อง
    ret, frame = cap.read()

    if not ret:
        print("ไม่สามารถรับภาพได้")
        break

    # แสดงภาพ
    cv2.imshow('Camera', frame)

    # กด 'q' เพื่อออกจากการแสดงผล
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ปิดการเชื่อมต่อกับกล้องและปิดหน้าต่างแสดงผล
cap.release()
cv2.destroyAllWindows()
