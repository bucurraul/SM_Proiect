from flask import Flask, render_template, Response, request
from threading import Lock
import cv2
import RPi.GPIO as GPIO
import imutils
import time

GPIO.setmode(GPIO.BCM)

GPIO.setup(26, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

servo = [GPIO.PWM(26, 50), GPIO.PWM(21, 50)]

lock = Lock()

LED = [20, 16]

GPIO.setup(LED[0], GPIO.OUT)
GPIO.setup(LED[1], GPIO.OUT)

state_led = [False, False]

app = Flask(__name__)

camera = [cv2.VideoCapture(0), cv2.VideoCapture(1)]

angles = [90, 90]

first_frame = None


@app.route('/')
def index():
    return render_template('index.html', n_cameras=2)


def trans_from_degrees(angle):
    return (angle/18.0) + 2.5


@app.route('/servo<n_camera>', methods=['POST'])
def get_dir(n_camera):
    n = int(n_camera)
    servo[n].start(0)
    time.sleep(0.5)
    angle = int(request.form['degrees'])
    angles[n] = angle

    duty = trans_from_degrees(180 - angle)

    servo[n].ChangeDutyCycle(duty)
    time.sleep(0.5)
    servo[n].stop()
    print('Changing angle to {} for camera {}'.format(angle, n))

    return "Ok"


@app.route("/get-angles", methods=["GET"])
def get_engals():
    return str(angles)


@app.route('/light<n_camera>', methods=['POST'])
def lumina(n_camera):
    global state_led

    n = int(n_camera)

    state_led[n] = not state_led[n]

    GPIO.output(LED[n], state_led[n])

    return "OK"


def gen(video):
    global first_frame

    while True:
        lock.acquire()

        _, frame = video.read()

        gray_scale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        gray_scale = cv2.GaussianBlur(gray_scale, (21,21), 0)

        if first_frame is None:
            first_frame = gray_scale

        frame_delta = cv2.absdiff(first_frame, gray_scale)
        threshold = cv2.threshold(frame_delta, 180, 255, cv2.THRESH_BINARY)[1]

        threshold = cv2.dilate(threshold, None, iterations=1)
        contours = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)

        for contour in contours:
            if cv2.contourArea(contour) < 600:
                continue

            (x,y,w,h) = cv2.boundingRect(contour)
            cv2.rectangle(frame, (x,y), (x+w, y+h), (0, 255, 0), 2)


        _, jpeg = cv2.imencode('.jpg', frame)
        first_frame = gray_scale
        res = (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

        lock.release()

        yield res


@app.route('/video_feed/<n_camera>')
def video_feed(n_camera):
    return Response(gen(camera[int(n_camera)]),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    
    duty = trans_from_degrees(90)
    
    servo[0].start(0)
    servo[1].start(0)
    time.sleep(2)    

    servo[0].ChangeDutyCycle(duty)
    servo[1].ChangeDutyCycle(duty)

    time.sleep(2)
    servo[0].stop()
    servo[1].stop()

    app.run(host='0.0.0.0',port='6969', debug=False)
