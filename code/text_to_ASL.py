import os.path


def a(text):
    words = text.split(' ')

    videos = []

    for word in words:
        path = '../database/' + word

        if os.path.exists(path):
            print('Found (', word, ') in database')
            # TODO check videos are in it
            print(os.listdir(path))
            folder_content = os.listdir(path)
            if len(folder_content) > 0:
                video_path = path + '/' + pick_video(folder_content)
                print(video_path)
                videos.append(video_path)

        else:
            print('Did not find (', word, ') in database')


def pick_video(folder_content):
    for item in folder_content:
        if item.endswith('.mp4'):
            return item
    return 'test'


if __name__ == "__main__":
    a('This is a test with a dog. a lot')
