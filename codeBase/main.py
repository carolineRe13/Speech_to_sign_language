import os
import re
import uuid

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, Response, g
from flask import request
from flask_cors import CORS

from codeBase.code.TextToASL import video_paths
from codeBase.code.VideoCreator import concatenate_videos
from codeBase.util.DeleteOldFiles import delete_files
from model.NLPKeywordExtraction import keyword_extraction_removed_from_sentence
from codeBase.code.SpeechToText import speech_to_text
from scipy.io.wavfile import read as read_wav

from google.cloud import speech
from google.cloud import storage

import atexit

VIDEO_RESULTS_FOLDER = '../results'


def get_speech_client():
    if 'speech_client' not in g:
        g.speech_client = speech.SpeechClient()

    return g.speech_client


def get_storage_client():
    if 'storage_client' not in g:
        g.storage_client = storage.Client()

    return g.storage_client


def create_app():
    # personal access, replace with access to your project json
    credential_path = "../keys/googleCloud.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path

    appp = Flask(__name__)

    return appp


app = create_app()


@app.teardown_appcontext
def teardown_speech_client(exception):
    g.pop('speech_client', None)
    g.pop('storage_client', None)


@app.route("/speech_to_ASL", methods=['POST'])
def speech_to_ASL():
    """
    Saves the recorded voice message and returns a unique video_id to identify the session
    """
    get_speech_client()
    get_storage_client()
    session_id = str(uuid.uuid4())
    f = request.files['audio_data']
    audio_file_name = session_id + '.wav'
    audio_file_path = '../results/' + audio_file_name
    with open(audio_file_path, 'wb') as audio:
        f.save(audio)
    sampling_rate, data = read_wav(audio_file_path)
    app.logger.info('file saved successfully')
    text = speech_to_text(audio_file_path, 'gs://speech_to_sign_bucket/' + audio_file_name, sampling_rate)

    # in case there are no results from the Google api
    if not text:
        return {}

    text_with_keywords = keyword_extraction_removed_from_sentence(app, text)
    video_paths_list = video_paths(text_with_keywords)
    print(video_paths_list)
    concatenate_videos(video_paths_list, VIDEO_RESULTS_FOLDER, session_id)

    return {
        "video_id": session_id
    }


@app.after_request
def after_request(response):
    """
    """
    response.headers.add('Accept-Ranges', 'bytes')
    return response


def get_chunk(video_id, byte1=None, byte2=None):
    """
    Returns the video in chunks
    """
    full_path = '../results/' + video_id + '.mp4'
    file_size = os.stat(full_path).st_size
    start = 0

    if byte1 < file_size:
        start = byte1
    if byte2:
        length = byte2 + 1 - byte1
    else:
        length = file_size - start

    with open(full_path, 'rb') as f:
        f.seek(start)
        chunk = f.read(length)
    return chunk, start, length, file_size


@app.route("/video/<video_id>")
def steam_resulting_video(video_id):
    """
    Streams the resulting video to the user
    """
    app.logger.info('video_id: ' + video_id)
    range_header = request.headers.get('Range', None)
    byte1, byte2 = 0, None
    if range_header:
        match = re.search(r'(\d+)-(\d*)', range_header)
        groups = match.groups()

        if groups[0]:
            byte1 = int(groups[0])
        if groups[1]:
            byte2 = int(groups[1])

    chunk, start, length, file_size = get_chunk(video_id, byte1, byte2)
    resp = Response(chunk, 206, mimetype='video/mp4',
                    content_type='video/mp4', direct_passthrough=True)
    resp.headers.add('Content-Range', 'bytes {0}-{1}/{2}'.format(start, start + length - 1, file_size))
    return resp


if __name__ == "__main__":
    scheduler = BackgroundScheduler()
    # calls the function delete_files every minute to delete old files
    scheduler.add_job(func=delete_files, trigger="interval", seconds=60)
    scheduler.start()

    cors = CORS(app, origins="*", send_wildcard=True, expose_headers='*')
    app.run(debug=True, threaded=True)

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
