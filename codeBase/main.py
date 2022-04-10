import uuid

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask import request

from codeBase.VideoCreator import concatenate_videos
from codeBase.TextToASL import video_paths
from codeBase.util.DeleteOldFiles import print_date_time
from model.NLPKeywordExtraction import keyword_extraction_removed_from_sentence
from SpeechToText import speech_to_text

import atexit

VIDEO_RESULTS_FOLDER = '../results'

app = Flask(__name__)


@app.route("/speech_to_ASL", methods=['POST'])
def speech_to_ASL():
    video_id = str(uuid.UUID)
    f = request.files['audio_data']
    with open('audio.wav', 'wb') as audio:
        f.save(audio)
    print('file saved successfully')
    text = speech_to_text('audio.wav', 'gs://speech_to_sign_bucket/audio.wav')
    text_with_keywords = keyword_extraction_removed_from_sentence(text)
    video_paths_list = video_paths(text_with_keywords)
    print(video_paths_list)
    concatenate_videos(video_paths_list, VIDEO_RESULTS_FOLDER, video_id)
    return video_id


@app.route("/video", methods=['GET'])
def steam_resulting_video(video_id):
    return "200"


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    scheduler.add_job(func=print_date_time(VIDEO_RESULTS_FOLDER), trigger="interval", seconds=60)
    scheduler.start()
    app.run(debug=True, threaded=True)

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
