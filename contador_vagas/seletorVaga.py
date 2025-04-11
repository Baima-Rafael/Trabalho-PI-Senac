import cv2
import numpy as np 

cap = cv2.VideoCapture(0)


while True:
    _,frame = cap.read()
    frame = frame[0:350, 15:540]
    cv2.imshow('Test', frame)
    vagas = 1
    for i in range(4):
        roi = cv2.selectROI("Select ROI", frame)
        x, y, w, h = roi
        cropped = frame[y:y+h, x:x+w]
        with open("roi.txt", "a") as file:
            file.write(f"'vagas{vagas}' : [{roi[0]},{roi[1]},{roi[2]},{roi[3]}]\n")
            vagas += 1
    key = cv2.waitKey(1)
    if key:
        break
cap.release()
cv2.destroyAllWindows()


