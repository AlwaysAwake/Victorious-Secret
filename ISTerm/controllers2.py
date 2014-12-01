import pyaudio
import wave
import base64
import requests
from flask import Flask, render_template, url_for, request

app = Flask(__name__)

c_id = ['']

def record():
    CHUNK = 1024
    FORMAT = pyaudio.paInt16 #paInt8
    CHANNELS = 2
    RATE = 44100 #sample rate
    RECORD_SECONDS = 5
    WAVE_OUTPUT_FILENAME = "output.wav"
    #WAVE_OUTPUT_FILENAME = url_for('static','res/output.wav')

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK) #buffer

    frames = []

    for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data) # 2 bytes(16 bits) per channel

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

@app.route('/', methods=['GET', 'POST'])
def main_page():
    if request.method == 'GET':
        return render_template("recognition.html")
    elif request.method == 'POST':
        pass

@app.route('/enroll', methods=['GET', 'POST'])
def enroll():
    payload = {'username': 'DnrHEZzghBNFnN2EhRaj', 'password': 'r7mJrrMMDvcCm7nJQMYaTYJz9Aape8', 'organisation_unit': 'd7965eb9-0e9f-45d2-9824-83335e2e21be'}
    r = requests.post("https://a9i1.voicevault.net/RestApi850/RegisterClaimant.ashx", params=payload)
    token = r.text.split("<claimant_id>")
    claimant_id = token[1].split("</claimant_id>")[0]
    c_id[0] = claimant_id

    payload = {'username': 'DnrHEZzghBNFnN2EhRaj', 'password': 'r7mJrrMMDvcCm7nJQMYaTYJz9Aape8', 'organisation_unit': 'd7965eb9-0e9f-45d2-9824-83335e2e21be' \
                   , 'claimant_id': claimant_id, 'language': 'EnglishUnitedStates', 'configuration_id': '93bf8f99-36b4-4e83-ae23-fc52dd47efa7'}
    r = requests.post("https://a9i1.voicevault.net/RestApi850/StartDialogue.ashx", params=payload)
    token = r.text.split("<dialogue_id>")
    dialogue_id = token[1].split("</dialogue_id>")[0]
    token = r.text.split("<prompt_hint>")
    prompt_hint = token[1].split("</prompt_hint>")[0]
    print prompt_hint
    token = r.text.split("<process_type>")
    process_type = token[1].split("</process_type>")



    #record()

    #f = open('output.wav', 'r')
    #content = f.read()
    #utterance = base64.b64encode(content)
    #print content
    files = {'utterance' : open('bombom.wav', 'r')}
    payload = {'username': 'DnrHEZzghBNFnN2EhRaj', 'password': 'r7mJrrMMDvcCm7nJQMYaTYJz9Aape8', 'dialogue_id': dialogue_id, \
                  'prompt': 'There are twenty-four hours in a day', 'format': 'Unknown'}
    r = requests.post("https://a9i1.voicevault.net/RestApi850/SubmitPhrase.ashx", params=payload, files = files)

    return render_template("recognition.html")

@app.route('/verify', methods=['GET', 'POST'])
def verify():
    payload = {'username': 'DnrHEZzghBNFnN2EhRaj', 'password': 'r7mJrrMMDvcCm7nJQMYaTYJz9Aape8', 'organisation_unit': 'd7965eb9-0e9f-45d2-9824-83335e2e21be' \
                   , 'claimant_id': c_id[0], 'language': 'EnglishUnitedStates', 'configuration_id': 'c05b41ae-9bc7-4402-b2e3-02dd81a94480'}
    r = requests.post("https://a9i1.voicevault.net/RestApi850/StartDialogue.ashx", params=payload)
    token = r.text.split("<dialogue_id>")
    dialogue_id = token[1].split("</dialogue_id>")[0]
    token = r.text.split("<prompt_hint>")
    prompt_hint = token[1].split("</prompt_hint>")[0]
    token = r.text.split("<process_type>")
    process_type = token[1].split("</process_type>")

#   record()

    #f = open('output.wav', 'r')
    #content = f.read()
    #utterance = base64.b64encode(content)
    #print content
    files = {'utterance' : open('bombom.wav', 'r')}
    payload = {'username': 'DnrHEZzghBNFnN2EhRaj', 'password': 'r7mJrrMMDvcCm7nJQMYaTYJz9Aape8', 'dialogue_id': dialogue_id, \
                  'prompt': prompt_hint, 'format': 'Unknown'}
    r = requests.post("https://a9i1.voicevault.net/RestApi850/SubmitPhrase.ashx", params=payload, files = files)

    return render_template("recognition.html")

if __name__ == '__main__':
    app.run(debug=True)