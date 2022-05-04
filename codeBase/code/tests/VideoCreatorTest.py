import os
import unittest

from codeBase.code.VideoCreator import create_video_with_text


class MyTestCase(unittest.TestCase):
    def test_video_created(self):
        database_path = 'database/'
        create_video_with_text('test', database_path)
        # create_or_update_database('/database')
        # self.assertEqual(True, False)  # add assertion here
        self.assertEqual(os.path.exists(database_path + '/test/text.mp4'), True)
        if os.path.exists(database_path):
            os.rmdir(database_path)


if __name__ == '__main__':
    unittest.main()
