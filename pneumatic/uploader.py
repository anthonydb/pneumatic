#!/usr/bin/env python

import os
import sys
import atexit
import json
import sqlite3
from multiprocessing import Pool
import requests
from colorama import init
from .db import Database
from .utils import Utils


class DocumentCloudUploader(object):
    """
    Main class containing functions to build and confirm file lists for
    uploading, make the upload requests, and later add metadata post-upload
    if desired.
    """

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.base_uri = 'https://' + username + ':' + password +\
                        '@www.documentcloud.org/api/'
        self.headers = {
            'User-Agent': 'pneumatic/0.1.8',
            'From': self.username
        }

        # Initialize colorama
        init()

        # Welcome users and test credentials
        print('\n\033[36mWelcome to pneumatic, a bulk uploader for ' +
              'DocumentCloud (https://www.documentcloud.org)\n\n' +
              'Initializing ...')
        if self.credential_test() == 200:
            print('\033[36m* Login credentials confirmed')
        else:
            print('\033[31mERROR: \033[0mYour username or password seems ' +
                  'to be incorrect.\nPlease check them and try again.\n\n' +
                  '\033[36mExiting pneumatic.\033[0m\n')
            sys.exit()

        # Initialize helper classes
        self.db = Database()
        self.utils = Utils()

        # Make the database that holds upload file data
        self.db.make_db()

        # Tasks to execute on program termination
        def cleanup(db_name):
            self.db.cleanup_empty_db(db_name)
            print('\n\033[36mExiting pneumatic.\033[0m\n')

        atexit.register(cleanup, self.db.db_full_path)

    def credential_test(self):
        """
        Confirm login credentials using simple search API endpoint.
        """
        print('\033[36m* Confirming your DocumentCloud login credentials')
        r = requests.get(self.base_uri + 'search.json?q=test')
        return r.status_code

    def log_exclusion(self, name, full_path, exclude_reason):
        """
        Log to the database a file excluded due to invalid file type
        or exceeding upload size limits.
        """
        timestamp = self.utils.timestamp()
        self.db.insert_row(
            None,            # id
            None,            # title
            name,
            full_path,
            timestamp,
            None,            # pages
            None,            # file hash
            None,            # result
            None,            # canonical_url
            None,            # pdf_url
            None,            # text_url
            'Y',             # exclude flag
            exclude_reason,
            None)            # error_msg

    def build_file_list(self, file_directory):
        """
        Walk the supplied or current directory, including sub-directories,
        and build a list of files for the upload. Report a file count to
        the user and give an option to proceed or not.
        """

        documents = []
        docs_to_upload = 0
        docs_to_exclude = 0

        print('\033[36m* Building a list of files to upload\n')

        # If no directory supplied, use the current directory.
        # If directory supplied, check that it exists.
        if not file_directory:
            file_directory = '.'
        else:
            directory_exists = self.utils.file_directory_check(file_directory)
            if not directory_exists:
                print('\n\033[31mERROR: \033[0mThe file directory ' +
                      'you supplied does not exist.\n' +
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

        # Count documents to upload and exclude.
        for doc in documents:
            if doc['exclude_flag']:
                docs_to_exclude += 1
            else:
                docs_to_upload += 1
        print('pneumatic found ' + str(docs_to_upload) +
              ' file(s) to upload. ' +
              str(docs_to_exclude) + ' file(s) will be excluded.')

        # Ask user to continue.
        response = input('Begin upload? Y/n: ')
        if response.lower() == 'y':
            pass
        else:
            sys.exit()

        return documents

    def request(self, upload_dict):
        """
        Post the request and log response to the database.
        """
        files = {'file': open(upload_dict['full_path'], 'rb')}
        print('\033[0m.. Uploading ' + upload_dict['full_path'])
        timestamp = self.utils.timestamp()

        # Upload via requests.
        r = requests.post(self.base_uri + 'upload.json',
                          params=upload_dict['payload'],
                          files=files,
                          headers=self.headers)

        # Check for success and set variables accordingly.
        if r.status_code == 200:
            upload_response = json.loads(r.text)
            print('\033[36m' + '++ Upload succeeded for ' +
                  upload_dict['full_path'])
            id = upload_response['id']
            title = upload_response['title']
            file_name = upload_dict['name']
            pages = upload_response['pages']
            file_hash = upload_response['file_hash']
            canonical_url = upload_response['canonical_url']
            pdf = upload_response['resources']['pdf']
            text = upload_response['resources']['text']
            error_msg = None
        else:
            print('\033[31m' + '!! Upload failed for ' +
                  upload_dict['full_path'])
            id = None
            title = None
            file_name = upload_dict['name']
            canonical_url = None
            pages = 0
            file_hash = None
            pdf = None
            text = None
            error_msg = r.text

        # Log upload response to the database.
        self.db.insert_row(
            id,
            title,
            file_name,
            upload_dict['full_path'],
            timestamp,
            pages,
            file_hash,
            r.status_code,
            canonical_url,
            pdf,
            text,
            'N',           # exclude_flag
            None,          # exclude_reason
            error_msg)     # error_msg

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
                if title:
                    upload_title = title
                else:
                    upload_title = os.path.splitext(doc['name'])[0]

                doc['payload'] = {
                    'title': upload_title,
                    'source': source,
                    'description': description,
                    'language': language,
                    'related_article': related_article,
                    'published_url': published_url,
                    'access': access,
                    'project': project,
                }
                # Thank you to Ben Welsh (@palewire):
                if data:
                    for key, value in data.items():
                        doc['payload']['data[%s]' % key] = value

                if secure:
                    if secure is True:
                        doc['payload']['secure'] = 'true'

                if force_ocr:
                    if force_ocr is True:
                        doc['payload']['force_ocr'] = 'true'

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

    def request_get(self, db, url):
        """
        Request a document and update the database with results
        """

        r = requests.get(url, headers=self.headers)

        if r.status_code == 200:
            # update db
            get_response = json.loads(r.text)

            id = get_response['document']['id']
            title = get_response['document']['title']
            pages = get_response['document']['pages']
            file_hash = get_response['document']['file_hash']

            self.db.update_row(
                db,
                id,
                title,
                None,          # file name
                None,          # file path
                None,          # timestamp
                pages,
                file_hash,
                None,          # status_code
                None,          # canonical_url
                None,          # pdf_url
                None,          # text_url
                None,          # exclude_flag
                None,          # exclude_reason
                None)          # error_msg

        else:
            print('\033[37mDocument not found\033[0m')

    def update_processed_files(self, db_name=None):
        """
        Retrieve each file's page count and file hash once
        DocumentCloud has finished processing the files.
        """

        # We can pass in a db name or use the one in the current session.
        # Check if it exists, first.
        if db_name:
            if os.path.isfile(db_name):
                db = db_name
            else:
                print('\033[31mERROR: \033[0mThe database file ' +
                      'specified does not exist.')
                sys.exit()
        else:
            db = self.db.db_full_path

        print('\n\033[36mUpdate Processed Files\n* Updating documents in ' + db + ' with page count ' +
              'and file hash data.')

        # Generate list of API get requests for successfully uploaded document
        conn = sqlite3.connect(db)
        cur = conn.cursor()
        uploaded_doc_urls = [self.base_uri + 'documents/' + row[0] + '.json'
                             for row in cur.execute('SELECT id FROM uploads WHERE result = 200;')]
        conn.close()

        for url in uploaded_doc_urls:
            self.request_get(db, url)
