import time

import cv2
cap = cv2.VideoCapture("rtsp://admin:1qaz2wsx@192.168.1.17:554/cam/realmonitor?channel=1&subtype=0")
ttt = 0
while True:
    print('time diff= ' + str(time.time() - ttt))
    ttt = time.time()
    ret, frame = cap.read()
    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
