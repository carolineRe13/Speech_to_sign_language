import os
import time


def print_date_time(folder):
    """
    deletes files that are older than 5 minutes
    """
    five_minute_ago = time.time() - 5 * 60
    os.chdir(folder)
    for file in os.listdir('..'):
        st = os.stat(file)
        file_age = st.st_mtime
        if file_age < five_minute_ago:
            os.unlink(file)
