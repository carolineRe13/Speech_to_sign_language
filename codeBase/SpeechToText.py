import os

from google.cloud import speech
from google.cloud import storage

from model.NLPKeywordExtraction import keyword_extraction_removed_from_sentence


def implicit():
    credential_path = r"C:\Users\Caroline\Documents\speechtosignlanguage-f7bb5dfe5dce.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


def upload_blob(bucket_name, source_file_name, destination_blob_name):
    """Uploads a file to the Google bucket."""

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


def speech_to_text(audio_file_name, gcs_uri):
    """Converts speech to text by using the Google api."""
    implicit()

    upload_blob("speech_to_sign_bucket", audio_file_name, os.path.basename(gcs_uri))
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=48000,
        audio_channel_count=2,
        language_code="en-US",
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=90)

    # Todo: check response in api
    for result in response.results:
        for alternative in result.alternatives:
            print(u"Transcript: {}".format(alternative.transcript))
            print("Confidence: {}".format(alternative.confidence))

    return response.results[0].alternatives[0].transcript
