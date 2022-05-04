import json

from moviepy.editor import *
from flask import app


# install ImageMagick
def add_text_to_video(file_path, dst, subtitle):
    """ Adds the name of the video folder as subtitle over the video duration
    Unfortunately, there is a bug in ffmpeg_reader.py
    Change infos = error.decode('utf8') in line 259 to:
    try:
    infos = error.decode('utf8')
        except:
    infos = error.decode('ANSI')
    """
    clip = VideoFileClip(file_path)
    # Generate a text clip

    txt_clip = TextClip(subtitle, fontsize=(clip.h * 40 / 540), color='grey')

    # setting position
    txt_clip = txt_clip.set_pos(('center', 'bottom')).set_duration(clip.duration)

    # Overlay the text clip on the first video clip
    video = CompositeVideoClip([clip, txt_clip])

    # Save video
    video.write_videofile(dst, fps=video.fps, temp_audiofile="temp-audio.m4a", remove_temp=True,
                          codec="mpeg4", audio_codec="aac")


# could replace generated text videos
def create_or_update_database(path):
    """ Adds videos to the db
    For every word, a folder is created. If a sign consists of more words, then the folders are created as tree
    hierarchies. For example; don't want has the folder structure: don't (can have videos for don't) -> want (has videos
    for don't want)
    If the word has a text generated video without sign, then its replaced by a sign video
    """
    args = sys.argv[1:]
    path_to_json = args[0]
    path_to_videos_folder = args[1]

    with open(path_to_json, 'r') as jsonFile:
        json_content = json.load(jsonFile)

        for word in json_content:
            current_word = word['gloss']

            app.logger.info(current_word + ' will be added')

            dst = path + '/'.join(current_word.split(' '))

            if not os.path.exists(dst):
                os.makedirs(dst)

            i = 0
            for instance in word['instances']:
                if instance['frame_end'] == -1:
                    src = path_to_videos_folder + '\\' + instance['video_id'] + '.mp4'

                    if os.path.exists(src):
                        add_text_to_video(src, dst + '/' + instance['video_id'] + '.mp4', current_word)
                        i += 1

            # remove text video
            folder_content = os.listdir(dst)
            videos = list(filter(lambda item: item.endswith('.mp4'), folder_content))
            if 'text.mp4' in videos:
                os.remove(dst + 'text.mp4')

            if i == 0:
                app.logger.info('no videos for', current_word)
                if len(os.listdir(dst)) == 0:
                    os.rmdir(dst)
            else:
                app.logger.info('video added for ', current_word)


if __name__ == "__main__":
    create_or_update_database('../../database/')
