import time


class Utils(object):
    """
    A few things we'll (eventually) use.
    """

    def __init__(self):
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
        Remove prohibited file types and files over upload size limit.
        """
        #TODO: Check file size; print list of excluded files.
        for x in doc_list:
            file_split = x.split('.')
            if file_split[-1] in self.file_excludes:
                doc_list.remove(x)
        return doc_list

    def timestamp(self):
        self.time = time.strftime("%Y%m%dT%H%M%S")
        return self.time
