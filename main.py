from flask import Flask
from flask import request

app = Flask(__name__)


@app.route("/", methods=['POST'])
def index():
    f = request.files['audio_data']
    with open('audio.wav', 'wb') as audio:
        f.save(audio)
    print('file uploaded successfully')

    return "200"


if __name__ == "__main__":
    app.run(debug=True)
