import cv2

def list_cameras(max_tests=10):
    available_cameras = []
    for i in range(max_tests):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW) # cv2.CAP_DSHOW is optional and specific to Windows
        if cap.isOpened():
            available_cameras.append(i)
            cap.release()
        else:
            break  # Stop if the camera cannot be opened
    return available_cameras

cameras = list_cameras()
print(f"Detected cameras: {cameras}")