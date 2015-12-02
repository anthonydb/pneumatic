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
        Remove prohibited file types and files over 400MB upload size limit.
        """
        doc_list_clean = []
        for x in doc_list:
            file_split = x['name'].split('.')
            if not file_split[-1] in self.file_excludes:
                if not os.path.getsize(x['full_path']) > 400000000:
                    doc_list_clean.append(x)
            print(os.path.getsize(x['full_path']))
        return doc_list_clean

    def timestamp(self):
        self.time = time.strftime("%Y%m%dT%H%M%S")
        return self.time
