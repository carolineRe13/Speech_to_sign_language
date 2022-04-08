from flask import Flask
from flask import request
from speechToText import speech_to_text

app = Flask(__name__)


@app.route("/", methods=['POST'])
def index():
    f = request.files['audio_data']
    with open('audio.wav', 'wb') as audio:
        f.save(audio)
    print('file uploaded successfully')
    speech_to_text('audio.wav', 'gs://speech_to_sign_bucket/audio.wav')

    return "200"


if __name__ == "__main__":
    app.run(debug=True)
