import cv2
import screeninfo

screen = screeninfo.get_monitors()[0]
w, h = screen.width, screen.height
"""
#set
centerX = int(width / 2)
centerY = int(height / 2)
radiusX = int(scale*centerX/100)
radiusY = int(scale*centerY/100)
minX = centerX - radiusX
maxX = centerX + radiusX
minY = centerY - radiusY
maxY = centerY + radiusY
"""
cap = cv2.VideoCapture() 
cap.open("http://192.168.1.38:8000/video")

wName = "Merrill Monitor"
cv2.namedWindow(wName, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(wName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

while(True):
    ret, frame = cap.read()
    frame = cv2.resize(frame, (w,h))
    #cv2.namedWindow(wName, cv2.WND_PROP_FULLSCREEN)
    #cv2.setWindowProperty(wName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

    cv2.imshow(wName,frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
