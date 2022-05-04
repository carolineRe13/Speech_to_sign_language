import os

from google.cloud import speech
from google.cloud import storage


def implicit():
    # personal access, replace with access to your project json
    credential_path = "../keys/googleCloud.json"
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path


def upload_blob(app, bucket_name, source_file_name, destination_blob_name):
    """ Uploads a file to the Google bucket. """

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    app.logger.info(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name)
    )


def speech_to_text(app, audio_file_name, gcs_uri, frame_rate):
    """ Converts speech to text by using the Google api.
    Text with highest confidence is returned or an empty string if there are no results.
    """
    implicit()

    upload_blob(app, "speech_to_sign_bucket", audio_file_name, os.path.basename(gcs_uri))
    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED,
        sample_rate_hertz=frame_rate,
        audio_channel_count=2,
        language_code="en-US",
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    response = operation.result(timeout=90)

    if len(response.results) < 1:
        return ""

    best_alternative = response.results[0].alternatives[0]

    print(response.results)

    for result in response.results:
        for alternative in result.alternatives:
            if alternative.confidence > best_alternative.confidence:
                best_alternative = alternative

    return best_alternative.transcript
