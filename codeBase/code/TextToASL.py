import os.path
import random


from codeBase.code.VideoCreator import create_video_with_text


def video_paths(text):
    """Returns video paths to all the words in text"""
    words = text.split(' ')

    return test(words, 0, '../database', '../../database', '')


def test(words, index, database, path, sign):
    if index == len(words):
        return []

    word = words[index]
    sign += ' ' + word
    sign = sign.strip(' ')

    current_path = path + '/' + word
    if not os.path.exists(current_path):
        os.mkdir(current_path)

    folder_content = os.listdir(current_path)
    subfolders = list(filter(lambda item: not item.endswith('.mp4'), folder_content))
    videos = list(filter(lambda item: item.endswith('.mp4'), folder_content))

    if len(subfolders) > 0 and index + 1 < len(words) and words[index+1] in subfolders:
        # app.logger.info('Found (', sign, words[index+1], ') in database')
        print('A Found (', sign, words[index+1], ') in database')
        return test(words, index+1, database, current_path, sign)
    elif len(videos) == 0:
        # app.logger.info('Creating (', sign, ') in database')
        print('Creating (', sign, ') in database')
        results = [create_video_with_text(sign), '../database/']
        results.extend(test(words, index + 1, database, database, ''))
        return results
    else:
        # app.logger.info('Found (', sign, ') in database')
        print('B Found (', sign, ') in database')
        results = [current_path + '/' + pick_video(videos)]
        results.extend(test(words, index + 1, database, database, ''))
        return results


def pick_video(videos):
    """Picks a random mp4 video from the folder"""
    return random.choice(videos)


if __name__ == "__main__":
    print(video_paths("don't care"))
