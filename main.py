from flask import Flask, render_template, Response, request
from threading import Lock
import cv2
import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)

GPIO.setup(26, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

servo = [GPIO.PWM(26, 50), GPIO.PWM(21, 50)]
servo[0].start(0)
servo[1].start(0)

lock = Lock()

LED = [20, 16]

GPIO.setup(LED[0], GPIO.OUT)
GPIO.setup(LED[1], GPIO.OUT)

state_led = [False, False]

app = Flask(__name__)

camera = [cv2.VideoCapture(0), cv2.VideoCapture(1)]

angles = [90, 90]


@app.route('/')
def index():
    return render_template('index.html', n_cameras=2)


def trans_from_degrees(angle):
    return (angle/18.0) + 2.5


@app.route('/servo/<n_camera>', methods=['POST'])
def get_dir(n_camera):
    n = int(n_camera)

    angle = int(request.form['degrees'])
    angles[int(n_camera)] = angle

    duty = trans_from_degrees(180 - angle)

    servo[n].ChangeDutyCycle(duty)

    return "Ok"


@app.route("/get-angles", methods=["GET"])
def get_engals():
    return str(angles)


@app.route('/light/<n_camera>', methods=['POST'])
def lumina(n_camera):
    global state_led
    n = int(n_camera)

    state_led[n] = not state_led[n]

    GPIO.output(LED[n], state_led[n])

    return "OK"


def gen(video):
    while True:
        lock.acquire()

        ret, frame = video.read()
        ret, jpeg = cv2.imencode('.jpg', frame)

        res = (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + jpeg.tobytes() + b'\r\n\r\n')

        lock.release()

        yield res


@app.route('/video_feed/<n_camera>')
def video_feed(n_camera):
    return Response(gen(camera[int(n_camera)]),mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    duty = trans_from_degrees(90)

    servo[0].ChangeDutyCycle(duty)
    servo[1].ChangeDutyCycle(duty)

    app.run(host='0.0.0.0',port='6969', debug=False)
