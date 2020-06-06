# main.py
# import the necessary packages
from flask import Flask, render_template, Response, redirect, request
from camera import VideoCamera
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
servo1 = GPIO.PWM(26,50)
servo1.start(0)

app = Flask(__name__)

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

def gen(camera):
    while True:
        #get camera frame
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    # defining server ip address and port
    app.run(host='0.0.0.0',port='5000', debug=False)
