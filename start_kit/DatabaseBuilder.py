import json
from moviepy.editor import *


# install ImageMagick
def add_text_to_video(file_path, dst, subtitle):
    """there is unfortunately a bug in ffmpeg_reader.py
    Change infos = error.decode('utf8') in line 259 to:
    try:
    infos = error.decode('utf8')
        except:
    infos = error.decode('ANSI')
    """
    clip = VideoFileClip(file_path)
    # Generate a text clip
    txt_clip = TextClip(subtitle, fontsize=(clip.w / len(subtitle)) - 1, color='grey')

    # setting position
    txt_clip = txt_clip.set_pos(('center', 'bottom')).set_duration(clip.duration)

    # Overlay the text clip on the first video clip
    video = CompositeVideoClip([clip, txt_clip])

    # Save video
    video.write_videofile(dst, fps=video.fps, temp_audiofile="temp-audio.m4a", remove_temp=True,
                           codec="mpeg4", audio_codec="aac")


# could replace generated text videos
def create_database():
    args = sys.argv[1:]

    path_to_json = args[0]
    path_to_videos_folder = args[1]

    with open(path_to_json, 'r') as jsonFile:
        json_content = json.load(jsonFile)

        for word in json_content:
            print(word['gloss'])

            dst = '../database/' + '/'.join(word['gloss'].split(' '))

            if not os.path.exists(dst):
                os.makedirs(dst)

            i = 0
            for instance in word['instances']:
                if instance['frame_end'] == -1:
                    src = path_to_videos_folder + '\\' + instance['video_id'] + '.mp4'

                    if os.path.exists(src):
                        add_text_to_video(src, dst + '/' + instance['video_id'] + '.mp4', word['gloss'])
                        i += 1

            if i == 0:
                print('no videos for', word['gloss'])
                if len(os.listdir(dst)) == 0:
                    os.rmdir(dst)


if __name__ == "__main__":
    create_database()
