import os

from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
from PIL import Image, ImageDraw
import moviepy.editor as mpy
import numpy as np


def concatenate_videos(video_clip_paths, output_folder_path, uuid, method="compose"):
    """ Concatenates several video files and save it to `output_path_folder`.
        `method` can be either 'compose' or 'reduce':
        `reduce`: Reduce the quality of the video to the lowest quality on the list of `video_clip_paths`.
        `compose`: type help(concatenate_videoclips) for the info
    """
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    # create VideoFileClip object for each video file
    clips = [VideoFileClip(c) for c in video_clip_paths]
    if method == "reduce":
        # calculate minimum width & height across all clips
        min_height = min([c.h for c in clips])
        min_width = min([c.w for c in clips])
        # resize the videos to the minimum
        clips = [c.resize(newsize=(min_width, min_height)) for c in clips]
        # concatenate the final video
        final_clip = concatenate_videoclips(clips)
    elif method == "compose":
        # concatenate the final video with the compose method provided by moviepy
        final_clip = concatenate_videoclips(clips, method="compose")
    # write the output video file
    final_clip.write_videofile(output_folder_path + '/' + uuid + '.mp4', fps=30, threads=1, codec="libx264")


def create_video_with_text(text):
    """if a word is missing then we create a video displaying the word"""
    output_folder_path = '../database/' + text

    img = Image.new('RGB', (640, 60), color=(0, 0, 0))

    d = ImageDraw.Draw(img)
    d.text((320, 40), text, fill=(211, 211, 211))

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
        col_opacity=1).set_duration(10)

    video_path = output_folder_path + '/text.mp4'
    video_with_text.write_videofile(video_path, fps=30, codec="mpeg4", audio_codec="aac")
    return video_path


if __name__ == "__main__":
    create_video_with_text('aa')
