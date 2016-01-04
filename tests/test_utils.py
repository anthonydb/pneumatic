#!/usr/bin/env python

import unittest
import tempfile
from pneumatic.utils import *


class TestFileSanitize(unittest.TestCase):

    def test_flag_file_type(self):
        """
        sanitize_uploads() should flag a prohibited file type
        with True in the returned exclude_flag field.
        """
        self.utils = Utils()
        files_dict_list = [{'name': 'SomeFile.mp3',
                            'full_path': '/path/SomeFile.mp3',
                            'exclude_flag': None,
                            'exclude_reason': None
                            }]
        docs = self.utils.sanitize_uploads(files_dict_list)
        self.assertTrue(docs[0]['exclude_flag'])

    def test_flag_file_size(self):
        """
        sanitize_uploads() should flag a file larger than 400MB
        with True in the returned exclude_flag field.
        """
        self.utils = Utils()
        with tempfile.NamedTemporaryFile(suffix='.pdf') as temp:
            temp.write(b'0' * 410000000)
            tempname = temp.name
            files_dict_list = [{'name': tempname,
                                'full_path': tempname,
                                'exclude_flag': None,
                                'exclude_reason': None
                                }]
            docs = self.utils.sanitize_uploads(files_dict_list)
            self.assertTrue(docs[0]['exclude_flag'])

if __name__ == '__main__':
    unittest.main()
