import os
import time


class Utils(object):
    """
    A few things we'll (eventually) use.
    """

    def __init__(self):
        # These are file types we do not want to send to DocumentCloud.
        self.file_excludes = (
            'aiff',
            'DS_Store',
            'flac',
            'mid',
            'mdb',
            'mp3',
            'ogg',
            'pst',
            'wav',
            'wma'
        )

    def sanitize_uploads(self, doc_list):
        """
        Flag prohibited file types and files over 400MB upload size limit.
        """
        for x in doc_list:
            file_split = x['name'].split('.')
            if file_split[-1] in self.file_excludes:
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
