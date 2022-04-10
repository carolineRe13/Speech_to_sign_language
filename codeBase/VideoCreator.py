import os

from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip
import gizeh as gz
import moviepy.editor as mpy


def concatenate_videos(video_clip_paths, output_folder_path, uuid, method="compose"):
    """Concatenates several video files into one video file
    and save it to `output_path`. Note that extension (mp4, etc.) must be added to `output_path`
    `method` can be either 'compose' or 'reduce':
        `reduce`: Reduce the quality of the video to the lowest quality on the list of `video_clip_paths`.
        `compose`: type help(concatenate_videoclips) for the info"""
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)

    output_path = output_folder_path + '/resultingVideo'

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


# install GTK+
def create_video_with_text(text):
    """if a word is missing then we create a video displaying the word"""
    output_folder_path = '../database/' + text

    def render_text(t):
        surface = gz.Surface(640, 60, bg_color=(0, 0, 0))
        # TODO doesnt work with text instead of 'test'
        text_object = gz.text(
            'test', fontfamily="Charter",
            fontsize=30, fontweight='bold', fill=(211, 211, 211), xy=(320, 40))
        text_object.draw(surface)
        return surface.get_npimage()

    text = mpy.VideoClip(render_text, duration=10)
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

    video_with_text.write_videofile(output_folder_path + '/text.mp4', fps=30, codec="mpeg4", audio_codec="aac")


if __name__ == "__main__":
    create_video_with_text('aa')
