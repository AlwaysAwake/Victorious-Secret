import requests
import hashlib

from flask import Flask, render_template, url_for, request, redirect, make_response

app = Flask(__name__)
app.config.from_object('settings.Config')

@app.route('/')
def main_page():
    return render_template("main.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")


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