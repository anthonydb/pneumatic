#!/usr/bin/env python

import os
import sys
import json
from multiprocessing import Pool
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
        self.utils = Utils()

    def credential_test(self):
        """
        Let's check the credentials with a simple search before
        lighting the fuse.
        """
        r = requests.get(self.base_uri + 'search.json?q=test')
        return r.status_code

    def log_exclusion(self, name, full_path, exclude_reason):
        """
        Log an excluded file to the database.
        """
        timestamp = self.utils.timestamp()
        self.db.insert_row(
            name,
            full_path,
            timestamp,
            None,
            None,
            'Y',
            exclude_reason)

    def build_file_list(self, file_directory):
        """
        Walk the supplied or current directory, including sub-directories,
        and build a list of files for the upload.
        """

        documents = []

        # If no directory supplied, use the current directory.
        # If directory supplied, check that it exists.
        if not file_directory:
            file_directory = '.'
        else:
            directory_exists = self.utils.file_directory_check(file_directory)
            if not directory_exists:
                print('The file directory you supplied does not exist.\n' +
                      'Please check it and try again.')
                sys.exit()

        # Create a list of dictionaries that includes file name and full path,
        # plus placeholders for exclusion information.
        files_dict_list = []
        for root, dir, files in os.walk(file_directory):
            for f in files:
                file_dict = {}
                file_dict['name'] = f
                file_dict['full_path'] = os.path.join(root, f)
                file_dict['exclude_flag'] = None
                file_dict['exclude_reason'] = None
                files_dict_list.append(file_dict)
        #print(files_dict_list) # for testing for now

        # Check list of files for prohibited formats, size
        documents = self.utils.sanitize_uploads(files_dict_list)
        return documents

    def request(self, upload_dict):
        """
        Post the request and log response to the database.
        """
        files = {'file': open(upload_dict['full_path'], 'rb')}

        print('Uploading ' + upload_dict['full_path'])
        r = requests.post(self.base_uri + 'upload.json', params=upload_dict['payload'], files=files)
        upload_response = json.loads(r.text)
        timestamp = self.utils.timestamp()
        self.db.insert_row(
            upload_response['title'],
            upload_dict['full_path'],
            timestamp,
            r.status_code,
            upload_response['canonical_url'],
            None,
            None)

    def upload(self, file_directory=None, title=None, source=None,
               description=None, language=None, related_article=None,
               published_url=None, access='private', project=None,
               data=None, secure=False, force_ocr=False):
        """
        Upload one or more documents with associated metadata and options.
        """
        # Start with a list of files in the supplied directory. Each
        # file is a dict.
        documents = self.build_file_list(file_directory)

        # Make the database
        self.db.make_db()
        self.db.print_db_name()

        # Appropriately process each file. Prohibited files will be
        # excluded and logged. The rest get added data and in the
        # list to be uploaded.
        cleared_uploads = []

        for doc in documents:
            if doc['exclude_flag']:
                self.log_exclusion(
                    doc['name'],
                    doc['full_path'],
                    doc['exclude_reason'])
            else:
                doc['payload'] = {
                    'title': doc['name'],
                    'source': source,
                    'description': description,
                    'language': language,
                    'related_article': related_article,
                    'published_url': published_url,
                    'access': access,
                    'project': project,
                    'secure': secure,
                    'force_ocr': force_ocr
                }
                # Thank you to Ben Welsh (@palewire) for the following two lines:
                for key, value in data.items():
                    doc['payload']['data[%s]' % key] = value

                # print(doc['payload'])
                cleared_uploads.append(doc)

        # Support multiprocessing on Linux-based systems
        if os.name == 'posix':
            # Create pool of workers. Just 4 for now, please.
            p = Pool(processes=4)
            p.map(self.request, cleared_uploads)
        # Otherwise, upload sequentially
        elif os.name == 'nt':
            for upload_dict in cleared_uploads:
                self.request(upload_dict)
