import os
import re
import uuid

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, Response
from flask import request

from codeBase.TextToASL import video_paths
from codeBase.VideoCreator import concatenate_videos
from codeBase.util.DeleteOldFiles import delete_files
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


@app.after_request
def after_request(response):
    response.headers.add('Accept-Ranges', 'bytes')
    return response


def get_chunk(video_id, byte1=None, byte2=None):
    full_path = 'result' + video_id + '.mp4'
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


@app.route("/video", methods=['GET'])
def steam_resulting_video(video_id):
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
    scheduler.add_job(func=delete_files, trigger="interval", seconds=60)
    scheduler.start()
    app.run(debug=True, threaded=True)

    # Shut down the scheduler when exiting the app
    atexit.register(lambda: scheduler.shutdown())
