import os
import sys
import hashlib

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'lib'))

import cv2
import requests

from lib.flask import Flask, render_template, jsonify, request

from lib.pyimagesearch.eyetracker import EyeTracker
from lib.pyimagesearch import imutils

from database import Database

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
        return render_template("signup.html", active_tab="signup")


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
                cv2.rectangle(frame, (rects[rect][0], rects[rect][1]), (rects[rect][2], rects[rect][3]), (0, 255, 255),1)
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
        return jsonify(result="ID isn't found. Try another ID.")


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
                cv2.rectangle(frame, (rects[rect][0], rects[rect][1]), (rects[rect][2], rects[rect][3]), (0, 255, 255),1)

        # show the tracked eyes and face
        cv2.imshow("Tracking", frame)

        # if the 'q' key is pressed, stop the loop
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
        if cv2.waitKey(1) & 0xFF == ord("a"):
            if (data[0]-0.2 < ratioGet(rects)[0] < data[0]+0.2) or (data[1]-0.14 < ratioGet(rects)[1] < data[1]+0.14) \
                or (data[2]-0.19 < ratioGet(rects)[2] < data[2]+0.19) or (data[3]-0.3 < ratioGet(rects)[3] < data[3]+0.3) \
                or (data[4]-0.15 < ratioGet(rects)[4] < data[4]+0.15):
                camera.release()
                cv2.destroyAllWindows()
                return jsonify(result='Success, Face Authenticated!')
            else:
                camera.release()
                cv2.destroyAllWindows()
                return jsonify(result='Fail!, Please Authenticate Again.')

    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()


@app.route('/voice_enroll', methods=['GET', 'POST'])
def voice_enroll():
    password = hashlib.sha256(app.config['PASSWD']).hexdigest()
    wavurl = request.form['url']
    userid = request.form['id']
    dbindex = next(index for (index, d) in enumerate(dataStorage.database) if d["id"] == userid)

    payload = {
        'VsitwavURL': wavurl,
        'VsitEmail': app.config['ADMINEMAIL'],
        'VsitPassword': password,
        'VsitDeveloperId': app.config['DEVELOPER_ID']
    }
    r = requests.post("https://siv.voiceprintportal.com/sivservice/api/enrollments/bywavurl", headers=payload)

    message = r.content.split(',')[0]
    enrollment_id = r.content.split('"')[7]

    if message.find("Success") != -1:
        dataStorage.database[dbindex]['voice'] = enrollment_id
        return jsonify(result="Voice Enrollment Succeeded!") # Success
    else:
        return jsonify(result="Try again!") # Failed


@app.route('/voice_verify', methods=['GET', 'POST'])
def voice_verify():
    password = hashlib.sha256(app.config['PASSWD']).hexdigest()
    wavurl = request.form['url']
    userid = request.form['id']
    accuracy = 3
    accuracyPasses = 5
    accuracyPassIncrement =3
    confidence = 89

    try:
        myindex = next(index for (index, d) in enumerate(dataStorage.database) if d["id"] == userid)
    except StopIteration:
        return jsonify(result="ID isn't found. Try another ID.")

    payload = {
        'VsitwavURL': wavurl,
        'VsitEmail': app.config['ADMINEMAIL'],
        'VsitPassword': password,
        'VsitDeveloperId': app.config['DEVELOPER_ID'],
        'VsitAccuracy': accuracy,
        'VsitAccuracyPasses': accuracyPasses,
        'VsitAccuracyPassIncrement': accuracyPassIncrement,
        'VsitConfidence': confidence
    }

    r = requests.post("https://siv.voiceprintportal.com/sivservice/api/authentications/bywavurl", headers=payload)

    message = r.content.split(',')[0]
    enrollment_id = r.content.split('"')[7]

    if dataStorage.database[myindex]['voice'] == enrollment_id and message.find("Authentication successful.") != -1:
        return jsonify(result="Voice Authentication Succeeded!") # Success
    elif message.find("Authentication failed.") != -1:
        return jsonify(result="Voice Authentication Failed!") # Failure
    else:
        return jsonify(result="Try again!")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("recognition.html", active_tab="login")
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