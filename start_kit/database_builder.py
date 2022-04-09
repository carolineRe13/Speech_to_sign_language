import os
import sys
import json
import shutil

if __name__ == "__main__":
    args = sys.argv[1:]

    path_to_json = args[0]
    path_to_videos_folder = args[1]

    with open(path_to_json, 'r') as jsonFile:
        aList = json.load(jsonFile)
        
        for word in aList:
            print(word['gloss'])

            dst = '../database/' + '/'.join(word['gloss'].split(' '))
    
            if not os.path.exists(dst):
                os.makedirs(dst)
    
            i = 0
            for instance in word['instances']:
                if instance['frame_end'] == -1:
                    src = path_to_videos_folder + '/' + instance['video_id'] + '.mp4'
    
                    if os.path.exists(src):
                        shutil.copy(src, dst)
                        i += 1
    
            if i == 0:
                print('no videos for', word['gloss'])
                if len(os.listdir(dst)) == 0:
                    os.rmdir(dst)
