import requests
import hashlib

from pyimagesearch.eyetracker import EyeTracker
from pyimagesearch import imutils
import cv2, os
from database import Database

from flask import Flask, render_template, jsonify, url_for, request, redirect, make_response

app = Flask(__name__)
app.config.from_object('settings.Config')

dataStorage = Database()

# getting the ratio of face
def ratioGet(rects):
   return [-(float(rects['face'][3]) - float(rects['eye'][1])/2 - float(rects['eye'][3])/2) / (float(rects['eye'][1])/2 + float(rects['eye'][3])/2 - float(rects['nose'][1])/2 - float(rects['nose'][3])/2), (float(rects['eye'][1])/2 + float(rects['eye'][3])/2 - float(rects['nose'][1])/2 - float(rects['nose'][3])/2) / (float(rects['nose'][1])/2+float(rects['nose'][3])/2 - float(rects['mouth'][1])/2 - float(rects['mouth'][3])/2), -(float(rects['nose'][1])/2 + float(rects['nose'][3])/2 - float(rects['mouth'][1])/2 - float(rects['mouth'][3])/2) / (float(rects['mouth'][1])/2+float(rects['mouth'][3])/2 - float(rects['face'][1])), (float(rects['eye'][2]-float(rects['eye'][0]))/(float(rects['mouth'][2])-float(rects['mouth'][0]))), (float(rects['face'][2]-float(rects['face'][0]))/(float(rects['eye'][2])-float(rects['eye'][0])))]

@app.route('/')
def main_page():
    return render_template("main.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")


@app.route('/faceregister', methods=['POST'])
def faceregister():
    id = request.form['id']
    camera = cv2.VideoCapture(0)
    # construct the eye tracker
    et = EyeTracker(os.path.dirname(os.path.abspath(__file__)))
    # if a video path was not supplied, grab the reference
    # to the gray
    dataInput = {}
    # keep looping
    while True:
        # grab the current frame
        (grabbed, frame) = camera.read()

        # resize the frame and convert it to grayscale
        frame = imutils.resize(frame, width=800)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces and eyes in the image
        rects = et.track(gray)

        # loop over the face bounding boxes and draw them
        for rect in rects:
            if rect == "face":
                cv2.rectangle(frame, (rects[rect][0], rects[rect][1]), (rects[rect][2], rects[rect][3]), (0, 255, 0), 1)
            if rect == "eye":
                cv2.rectangle(frame, (rects[rect][0], rects[rect][1]), (rects[rect][2], rects[rect][3]), (255, 0, 0), 1)
            if rect == "mouth":
                cv2.rectangle(frame, (rects[rect][0], rects[rect][1]), (rects[rect][2], rects[rect][3]), (0, 0, 255), 1)
            if rect == "nose":
                cv2.rectangle(frame, (rects[rect][0], rects[rect][1]), (rects[rect][2], rects[rect][3]), (0, 255, 255),
                              1)
        # show the tracked eyes and face
        cv2.imshow("Tracking", frame)

        if cv2.waitKey(1) & 0xFF == ord("r"):
            dataInput['id'] = id
            dataInput['face'] = ratioGet(rects)
            dataStorage.put(dataInput)
            break

    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()

    return jsonify(result='Face Enrollment Succeed!')


@app.route('/faceauth', methods=['POST'])
def faceauth():
    flag = False
    id = request.form['id']
    camera = cv2.VideoCapture(0)
    # construct the eye tracker
    et = EyeTracker(os.path.dirname(os.path.abspath(__file__)))
    dataout = dataStorage.out()
    data = []

    for i in dataout:
        if i['id'] == id:
            data = i['face']
            flag = True
    if flag == False:
        return jsonify(result ='Fail')


    while True:
        # grab the current frame
        (grabbed, frame) = camera.read()

        # resize the frame and convert it to grayscale
        frame = imutils.resize(frame, width=800)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # detect faces and eyes in the image
        rects = et.track(gray)

        # loop over the face bounding boxes and draw them
        for rect in rects:
            if rect == "face":
                cv2.rectangle(frame, (rects[rect][0], rects[rect][1]), (rects[rect][2], rects[rect][3]), (0, 255, 0), 1)
            if rect == "eye":
                cv2.rectangle(frame, (rects[rect][0], rects[rect][1]), (rects[rect][2], rects[rect][3]), (255, 0, 0), 1)
            if rect == "mouth":
                cv2.rectangle(frame, (rects[rect][0], rects[rect][1]), (rects[rect][2], rects[rect][3]), (0, 0, 255), 1)
            if rect == "nose":
                cv2.rectangle(frame, (rects[rect][0], rects[rect][1]), (rects[rect][2], rects[rect][3]), (0, 255, 255),
                              1)

        # show the tracked eyes and face
        cv2.imshow("Tracking", frame)

        # if the 'q' key is pressed, stop the loop
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        if cv2.waitKey(1) & 0xFF == ord("a"):
            i = 0
            for x in data:
                if (x - 0.19 < ratioGet(rects)[i] < x + 0.19):
                    i = i + 1
                else:
                    camera.release()
                    cv2.destroyAllWindows()
                    return jsonify('Fail!, Please Authenticate Again.')
                    break
            if i == 5:
                # cleanup the camera and close any open windows
                camera.release()
                cv2.destroyAllWindows()
                return jsonify('Success, Face Authenticated!')
            break
    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()


@app.route('/voice', methods=['POST'])
def voice():
    url = "https://siv.voiceprintportal.com/sivservice/api/enrollments/bywavurl"
    print request.form['email']
    wavurl = ""
    """
    passwd = hashlib.sha256(request.form['passwd']).hexdigest()
    firstname = request.form['firstname']
    lastname = request.form['lastname']
    phone = request.form['phone']

    payload = {
        'VsitEmail': email,
        'VsitPassword': passwd,
        'VsitDeveloperId': app.config['DEVELOPER_ID'],
        'VsitFirstName': firstname,
        'VsitLastName': lastname,
        'VsitPhone1': phone
    }
    """
    """
    payload = {
        'VsitEmail': email,
        'VsitPassword': hashlib.sha256(app.config['PASSWORD']).hexdigest(),
        'VsitDeveloperId': app.config['DEVELOPER_ID'],
        'VsitwavURL': wavurl
    }

    r = requests.post(url, headers=payload)
    """
    return make_response("success")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("recognition.html")
    elif request.method == 'POST':
        pass

#
# @ Error Handlers
#
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True)