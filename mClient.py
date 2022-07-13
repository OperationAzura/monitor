import cv2

cap = cv2.VideoCapture() 
cap.open("http://192.168.1.38:8000/video")

while(True):
    ret, frame = cap.read()

    cv2.imshow('Monitor',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
