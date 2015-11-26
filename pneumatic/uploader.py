import os
import sys
import json
import requests
from .db import Database
from .utils import Utils


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
            print('Your username or password is incorrect.\n' +
                  'Please check them and try again.')
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
        print(r.status_code)
        print(r.text)
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

        # Create a list of dictionaries that includes file name and full path
        files_dict_list = []
        for root, dir, files in os.walk(file_directory):
            for f in files:
                file_dict = {}
                file_dict['name'] = f
                file_dict['full_path'] = os.path.join(root, f)
                files_dict_list.append(file_dict)
        print(files_dict_list)

        # Remove files with prohibited formats
        documents = self.utils.sanitize_uploads(files_dict_list)

        for doc in documents:
            print('Uploading ' + doc['full_path'])
            payload = {
                'title': doc['name'],
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
            upload = {'file': open(doc['full_path'], 'rb')}
            print(payload)
            self.request(payload, upload)
