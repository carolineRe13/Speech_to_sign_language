import os
import time

TIME = time.time() - 5 * 60
USER_AUDIO_FILE = 'audio.wav'


def delete_old_files():
    """
        deletes resulting videos and a user's audio file that are older than TIME
    """
    os.chdir('../results')
    for file in os.listdir('../results'):
        delete_file(file)
    if os.path.exists(USER_AUDIO_FILE):
        delete_file(USER_AUDIO_FILE)


def delete_file(file):
    """
        deletes the file if it's older than TIME
    """
    st = os.stat(file)
    file_age = st.st_mtime
    if file_age < TIME:
        os.unlink(file)
