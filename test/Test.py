from ast import literal_eval
from io import BytesIO

import pytest
from contextlib import contextmanager
from flask import appcontext_pushed, g
from unittest.mock import MagicMock

from codeBase.main import app
from unittest.mock import patch


@contextmanager
def clients_set(speech_client, storage_client):
    def handler(sender, **kwargs):
        g.speech_client = speech_client
        g.storage_client = storage_client

    with appcontext_pushed.connected_to(handler, app) as context:
        yield context


@pytest.fixture()
def client():
    with app.test_client() as client:
        yield client


@patch('google.api_core.operation.Operation')
@patch('google.cloud.speech.SpeechClient')
@patch('google.cloud.storage.Client')
def test_request_example(MockStorage, MockSpeech, MockOperation, client):
    speech_client = MockSpeech()
    storage_client = MockStorage()
    with clients_set(speech_client, storage_client):
        with open("./resources/test.wav", "rb") as audio_file:
            buf = BytesIO(audio_file.read())

        data = dict(
            audio_data=(buf, "test.wav"),
        )

        op = MockOperation()

        op.result = MagicMock(return_value=Response([Result([Alternative("aaaaa", 99.0)])]))

        speech_client.long_running_recognize = MagicMock(return_value=op)

        response = client.post("/speech_to_ASL", data=data)

        video_id = literal_eval(response.data.decode('utf-8'))["video_id"]

        response = client.get("/video/" + video_id)
        assert response.status_code == 206




class Response:
    results = []

    def __init__(self, results):
        self.results = results


class Result:
    alternatives = []

    def __init__(self, alternatives):
        self.alternatives = alternatives


class Alternative:
    transcript = ""
    confidence = 0.0

    def __init__(self, transcript, alternative):
        self.transcript = transcript
        self.confidence = alternative
