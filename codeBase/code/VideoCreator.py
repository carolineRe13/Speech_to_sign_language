import os

from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
from PIL import ImageFont, Image, ImageDraw
import moviepy.editor as mpy
import numpy as np

WIDTH = 960
HEIGHT = 540


def concatenate_videos(video_clip_paths, output_folder_path, uuid):
    """ Concatenates several video files and save it to `output_path_folder`.
        `method` can be either 'compose' or 'reduce':
        `reduce`: Reduce the quality of the video to the lowest quality on the list of `video_clip_paths`.
        `compose`: type help(concatenate_videoclips) for the info
    """
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # create VideoFileClip object for each video file
    clips = [VideoFileClip(c) for c in video_clip_paths]

    # resize the videos to the maximum
    clips = [c.resize(newsize=(WIDTH, HEIGHT)) for c in clips]
    # concatenate the final video
    final_clip = concatenate_videoclips(clips)

    # write the output video file
    final_clip.write_videofile(output_folder_path + '/' + uuid + '.mp4', fps=24, threads=1, codec="libx264")


def create_video_with_text(text, database_path):
    """if a word is missing then we create a video displaying the word"""
    output_folder_path = database_path + "/" + text

    img = Image.new('RGB', (WIDTH, HEIGHT), color=(0, 0, 0))

    d = ImageDraw.Draw(img)

    font = ImageFont.truetype("arial.ttf", 40)
    d.text((WIDTH/2, HEIGHT/2), text, font=font, fill=(255, 255, 255), anchor="mm")

    pixels = list(img.getdata())
    width, height = img.size
    pixels = [pixels[i * width:(i + 1) * width] for i in range(height)]

    frame = np.asarray(pixels)

    def make_frame(t):
        return frame

    text = mpy.VideoClip(make_frame, duration=1)

    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    video_with_text = mpy.CompositeVideoClip(
        [
            text.set_position(("center", "top"))
        ],
        size=(640, 480)). \
        on_color(
        color=(0, 0, 0),
        col_opacity=1).set_duration(1)

    video_path = output_folder_path + '/text.mp4'
    video_with_text.write_videofile(video_path, fps=30, codec="mpeg4", audio_codec="aac")
    return video_path


if __name__ == "__main__":
    create_video_with_text('aa')
