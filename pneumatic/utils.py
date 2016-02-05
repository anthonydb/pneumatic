#!/usr/bin/env python

import os
import time
from .excludes import file_excludes


class Utils(object):
    """
    A few things we'll (eventually) use.
    """

    def __init__(self):
        self.file_excludes = file_excludes

    def file_directory_check(self, file_directory):
        dir_exists = os.path.isdir(file_directory)
        return dir_exists

    def sanitize_uploads(self, doc_list):
        """
        Flag prohibited file types and files over 400MB upload size limit.
        """
        for x in doc_list:
            file_split = x['name'].split('.')
            if file_split[-1].lower() in self.file_excludes:
                x['exclude_flag'] = True
                x['exclude_reason'] = 'Prohibited file type'
            elif os.path.getsize(x['full_path']) > 400000000:
                x['exclude_flag'] = True
                x['exclude_reason'] = 'File over 400MB'
            else:
                x['exclude_flag'] = False
        return doc_list

    def timestamp(self):
        self.time = time.strftime("%Y%m%dT%H%M%S")
        return self.time
