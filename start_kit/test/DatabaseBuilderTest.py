import os
import unittest

from codeBase.code.VideoCreator import create_video_with_text
from start_kit.code.DatabaseBuilder import create_or_update_database


class DatabaseBuilder(unittest.TestCase):
    def test_text_video_is_replaced(self):
        database_path = 'database/'
        create_video_with_text('test', database_path)
        self.assertEqual(os.path.exists(database_path + '/test/text.mp4'), True)
        create_or_update_database('/database')
        # if os.path.exists(database_path):
        #    os.rmdir(database_path)


if __name__ == '__main__':
    unittest.main()
