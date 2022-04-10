import os.path

from codeBase.VideoCreator import concatenate_videos, create_video_with_text


def video_paths(text):
    words = text.split(' ')

    videos = []

    multiple_words = ""

    for word in words:
        path = '../database/' + word

        if os.path.exists(path):
            print('Found (', word, ') in database')
            print(os.listdir(path))
            folder_content = os.listdir(path)
            if len(folder_content) > 0:  # TODO handle folders with sub-folders "come here"
                video_path = path + '/' + pick_video(folder_content)
                print(video_path)
                videos.append(video_path)

        else:
            print('Did not find (', word, ') in database')
            create_video_with_text(word)
            videos.append(path + '.mp4')
    return videos


def pick_video(folder_content):
    for item in folder_content:
        if item.endswith('.mp4'):
            return item
    return 'test'


if __name__ == "__main__":
    # video_paths('This is a test with a dog. a lot')
    paths = video_paths('This is a test with a dog.')
    concatenate_videos(paths, '../results')
