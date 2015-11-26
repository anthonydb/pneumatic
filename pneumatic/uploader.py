import os
import sys
import json
import requests
from db import Database
from utils import Utils

# TODO
# Database methods to dump a CSV
# test for status codes and react accordingly
# multiprocessing
# default upload current directory (but exclude .py)
# exclude files of a certain size or filetype we don't want


class DocumentCloudUploader(object):
    """
    The main thing.
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.base_uri = 'https://' + username + ':' + password +\
                        '@www.documentcloud.org/api/'

        if self.credential_test() == 200:
            pass
        else:
            print 'Your username or password is incorrect.\n' +\
                  'Please check them and try again.'
            sys.exit()

        self.db = Database()
        self.db.print_db_name()
        self.utils = Utils()

    def credential_test(self):
        """
        Let's check the credentials with a simple search before
        lighting the fuse.
        """
        r = requests.get(self.base_uri + 'search.json?q=test')
        return r.status_code

    def request(self, payload, upload):
        """
        Post the request.
        """
        r = requests.post(self.base_uri + 'upload.json', data=payload, files=upload)
        print r.status_code
        print r.text
        upload_response = json.loads(r.text)
        timestamp = self.utils.timestamp()
        self.db.insert_row(
            upload_response['title'],
            timestamp,
            r.status_code,
            upload_response['canonical_url'])

    def upload(self, file_directory=None, title=None, source=None,
               description=None, language=None, related_article=None,
               published_url=None, access='private', project=None,
               data=None, secure=False):
        """
        Upload one or more documents with associated metadata and options.
        """

        # Walk the supplied or current directory, including sub-directories,
        # and build a list of files for the upload
        documents = []
        if not file_directory:
            file_directory = '.'

# MAKE THIS A LIST OF DICTS WITH FULL PATH, FILE NAME SEPARATE
        for root, dir, files in os.walk(file_directory):
            for f in files:
                documents.append(os.path.join(root, f))

        # Remove files with prohibited formats
        documents = self.utils.sanitize_uploads(documents)

        for doc in documents:
            print 'Uploading ' + doc
            payload = {
                'title': doc,
                'source': source,
                'description': description,
                'language': language,
                'related_article': related_article,
                'published_url': published_url,
                'access': access,
                'project': project,
                'data': data,
                'secure': secure
            }
            upload = {'file': open(doc, 'rb')}
            print payload
            #self.request(payload, upload)
