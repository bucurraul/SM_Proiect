# main.py
# import the necessary packages
from flask import Flask, render_template, Response, redirect, request
from camera import VideoCamera
from threading import Lock
import cv2
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
servo0 = GPIO.PWM(26,50)
servo0.start(0)

GPIO.setup(21, GPIO.OUT)
servo1 = GPIO.PWM(21,50)
servo1.start(0)

lock = Lock()

LED_0 = 20
LED_1 = 16

GPIO.setup(LED_0, GPIO.OUT)
GPIO.setup(LED_1, GPIO.OUT)

state_led_0 = False
state_led_1 = False

app = Flask(__name__)

video0 = cv2.VideoCapture(0)
video1 = cv2.VideoCapture(1)

@app.route('/')
def index():
    return render_template('index.html')

def trans_from_degrees(angle):
    return (angle/18.0) + 2.5
   
angles = [90, 90]

@app.route('/servo0', methods=['POST'])
def get_dir0():
    angle = int(request.form['degrees'])
    angles[0] = angle
    duty = trans_from_degrees(180 - angle)
    servo0.ChangeDutyCycle(duty)
    
    return "Ok"

@app.route('/servo1', methods=['POST'])
def get_dir1():
    angle = int(request.form['degrees'])
    angles[1] = angle
    duty = trans_from_degrees(180 - angle)
    servo1.ChangeDutyCycle(duty)
    
    return "Ok"
    

@app.route("/get-angles", methods=["GET"])
def get_engals():
    return str(angles)


@app.route('/light0', methods=['POST'])
def lumina_0():
    global state_led_0
    state_led_0 = not state_led_0
    GPIO.output(LED_0, state_led_0)
    
    return "OK"

@app.route('/light1', methods=['POST'])
def lumina_1():
    global state_led_1
    state_led_1 = not state_led_1
    GPIO.output(LED_1, state_led_1)
    
    return "OK"


def gen(video):
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

@app.route('/video_feed0')
def video_feed0():
    return Response(gen(video0),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video_feed1')
def video_feed1():
    return Response(gen(video1),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # defining server ip address and port
    duty = trans_from_degrees(90)

    servo1.ChangeDutyCycle(duty)
    servo1.ChangeDutyCycle(duty)

    app.run(host='0.0.0.0',port='6969', debug=False)
