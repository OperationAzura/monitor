import cv2
import pexpect
import time
import threading
from flask import Flask, Response,render_template
import pyaudio
print('yep')
child = pexpect.spawn('sudo service nvargus-daemon restart')
child.expect('password')
child.sendline('bazinga1')
time.sleep(1)
print('balls')
# Image frame sent to the Flask object
global video_frame
video_frame = None

# Use locks for thread-safe viewing of frames in multiple browsers
global thread_lock 
thread_lock = threading.Lock()

global statusLock
statusLock = threading.Lock()
global status
status = 'None'
# GStreamer Pipeline to access the Raspberry Pi camera
GSTREAMER_PIPELINE = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=1280, height=720, format=(string)NV12, framerate=60/1 ! nvvidconv flip-method=2 ! video/x-raw, width=640, height=360, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink wait-on-eos=false max-buffers=1 drop=True'

# Create the Flask object for the application
app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('mx.html')

@app.route('/status')
def getStatus():
    global statusLock
    with statusLock:
        global status
        return status
def captureFrames():
    global video_frame, thread_lock
    frameCountTick = 5
    frameCount = frameCountTick + 1
    # Video capturing from OpenCV
    cap = cv2.VideoCapture(GSTREAMER_PIPELINE, cv2.CAP_GSTREAMER)
    #frames for motion detection
    while not cap.isOpened():
        pass
    firstFrame = None
    firstGray = None
    while True:
        retKey, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (21, 21), 0)

        if frameCount > frameCountTick:
            firstGray = gray
            frameCount = 0
            continue
        else:
            frameCount += 1

        deltaFrame = cv2.absdiff(firstGray, gray)
        thresh = cv2.threshold(deltaFrame, 25, 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        cnts, h = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        totalArea = 0
        for c in cnts:
            totalArea += cv2.contourArea(c)
        cv2.drawContours(frame, cnts, -1, (0, 255, 0), 3)
        global statusLock
        with statusLock:
            global status
            status =  str(totalArea)

        if not retKey:
            break

        # Create a copy of the frame and store it in the global variable,
        # with thread safe access
        with thread_lock:
            video_frame = frame.copy()
        
        key = cv2.waitKey(30) & 0xff
        if key == 27:
            break

    cap.release()
        
def encodeFrame():
    global thread_lock
    while True:
        # Acquire thread_lock to access the global video_frame object
        with thread_lock:
            global video_frame
            if video_frame is None:
                continue
            retKey, encoded_image = cv2.imencode(".jpg", video_frame)
            if not retKey:
                continue

        # Output image as a byte array
        yield(b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' + 
            bytearray(encoded_image) + b'\r\n')

@app.route("/video")
def video():
    return Response(encodeFrame(), mimetype = "multipart/x-mixed-replace; boundary=frame")

# check to see if this is the main thread of execution
if __name__ == '__main__':

    # Create a thread and attach the method that captures the image frames, to it
    process_thread = threading.Thread(target=captureFrames)
    process_thread.daemon = True

    # Start the thread
    process_thread.start()

    # start the Flask Web Application
    # While it can be run on any feasible IP, IP = 0.0.0.0 renders the web app on
    # the host machine's localhost and is discoverable by other machines on the same network 
    app.run("0.0.0.0", port="8000")
