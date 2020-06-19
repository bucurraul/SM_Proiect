# main.py
# import the necessary packages
from flask import Flask, render_template, Response, redirect, request
from camera import VideoCamera
from threading import Lock
import cv2
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
servo1 = GPIO.PWM(26,50)
servo1.start(0)

lock = Lock()

app = Flask(__name__)

video = cv2.VideoCapture(0)

@app.route('/')
def index():
    return render_template('index.html')

def trans_from_degrees(angle):
    return (angle/18.0) + 2.5
    
@app.route('/servo', methods=['POST'])
def get_dir():
    angle = int(request.form['degrees'])
    duty = trans_from_degrees(angle)
    servo1.ChangeDutyCycle(duty)
    
    return "Ok"

def gen():
    while True:

        lock.acquire()

        ret, frame = video.read()
            # frame = cv2.resize(frame, None, fx=ds_factor, fy=ds_factor,
                           # interpolation=cv2.INTER_AREA)
        ret, jpeg = cv2.imencode('.jpg', frame)

        res = (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')
        # video.release()

        lock.release()

        yield res

@app.route('/video_feed')
def video_feed():
    return Response(gen(),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # defining server ip address and port
    app.run(host='0.0.0.0',port='6969', debug=False)
