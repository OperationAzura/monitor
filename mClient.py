import cv2
import screeninfo
import time

screen = screeninfo.get_monitors()[0]
w, h = screen.width, screen.height

cap = cv2.VideoCapture("http://192.168.1.38:8000/video")
cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
#cap.open("http://192.168.1.38:8000/video")

wName = "Merrill Monitor"
cv2.namedWindow(wName, cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty(wName, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)

font = cv2.FONT_HERSHEY_SIMPLEX

org = (25, 75)
orgFCount = (25, 175)
fontScale = 3

color = (0, 255, 0)

thickness = 3

fCount = 1
fLimit = 30
fps = 11111111111111111111
fTime = time.time()
while(True):
    if fCount == 1:
        fTime = time.time()
    elif fCount == fLimit:
        cap.release()
        fCount = 1
        fps = fLimit / (time.time() - fTime)
        cap = cv2.VideoCapture('http://192.168.1.38:8000/video')
        cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
    fCount += 1
    #s = time.time()
    _, frame = cap.read()
    frame = cv2.resize(frame, (w,h))
    #print('read and resize: ', (time.time() - s))
    #frame = cv2.putText(frame, 'fCount: '+str(fCount), orgFCount, font, fontScale, color, thickness, cv2.LINE_AA)
    frame = cv2.putText(frame, 'FPS: '+str(fps), org, font, fontScale, color, thickness, cv2.LINE_AA)
    cv2.imshow(wName,frame)
    #cap.release()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
