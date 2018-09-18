#!/usr/bin/env python

import os
import sys
import csv
import sqlite3
from colorama import init
from .utils import Utils


class Database(object):
    """
    A SQLite database to store results of file upload attempts to
    DocumentCloud, along with database-related utilities.
    """

    def __init__(self):
        self.utils = Utils()

        # Initialize colorama
        init()

    def make_db(self):
        # Create a SQLite db whose name includes a timestamp.
        timestamp = self.utils.timestamp()
        self.db_name = 'dc-upload-' + timestamp + '.db'

        # make the database file directory
        if not os.path.isdir('pneumatic_db'):
            os.mkdir('pneumatic_db')
        else:
            pass
        self.db_full_path = os.path.join('pneumatic_db', self.db_name)

        # Connect to the db and create the uploads table.
        if not os.path.exists(self.db_full_path):
            conn = sqlite3.connect(self.db_full_path)
            cur = conn.cursor()
            cur.execute('''
                CREATE TABLE uploads
                (
                    id Text, title Text, file_name Text, full_path Text,
                    upload_time Text, pages Integer, file_hash Text,
                    result Text, canonical_url Text, pdf_url Text,
                    text_url Text, exclude_flag Text, exclude_reason Text,
                    error_msg Text
                )
                       ''')
            conn.commit()
            conn.close()
            print('\033[36m* New uploads database created at: ' +
                  self.db_full_path)
        else:
            pass

    def insert_row(self, id, title, file_name, full_path, up_time, pages,
                   file_hash, result, canonical_url, pdf_url, text_url,
                   exclude_flag, exclude_reason, error_msg):
        """
        Inserts a row in the table.
        """
        conn = sqlite3.connect(self.db_full_path)
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO uploads VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?);
            ''', (id, title, file_name, full_path, up_time, pages,
                  file_hash, result, canonical_url, pdf_url, text_url,
                  exclude_flag, exclude_reason, error_msg))
        conn.commit()
        conn.close()

    def update_row(self, db, id, title, file_name, full_path, up_time, pages,
                   file_hash, result, canonical_url, pdf_url, text_url,
                   exclude_flag, exclude_reason, error_msg):
        """
        Updates a row in the table.
        """
        conn = sqlite3.connect(db)
        cur = conn.cursor()

        cur.execute('''
            UPDATE uploads
            SET title = ?, pages = ?, file_hash = ?
            WHERE id = ?;
            ''', (title, pages, file_hash, id))
        conn.commit()
        conn.close()

    def dump_to_csv(self, db_name=None):
        """
        Outputs the contents of a SQLite database to CSV.
        """
        print('\n\033[36mDump to CSV')

        timestamp = self.utils.timestamp()

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
            db = self.db_full_path

        # Create an output folder and CSV file name.
        if not os.path.isdir('pneumatic_csv'):
            os.mkdir('pneumatic_csv')
        else:
            pass
        self.csv_name = 'dc-output-' + timestamp + '.csv'
        self.csv_full_path = os.path.join('pneumatic_csv', self.csv_name)

        # Query the database and write the rows to the CSV.
        row_counter = 0
        with open(self.csv_full_path, 'w', newline='') as csvfile:
            header_row = ('id', 'title', 'file_name', 'full_path',
                          'upload_time', 'pages', 'file_hash', 'result',
                          'canonical_url', 'pdf_url', 'text_url',
                          'exclude_flag', 'exclude_reason', 'error_msg')

            writer = csv.writer(csvfile, delimiter=',', quotechar='"')
            writer.writerow(header_row)

            # Query the database and write rows to CSV.
            conn = sqlite3.connect(db)
            cur = conn.cursor()
            for row in cur.execute('SELECT * FROM uploads;'):
                writer.writerow(row)
                row_counter += 1
            conn.close()

        print('\033[36m* CSV file created. ' + str(row_counter) +
              ' database records were exported to ' + self.csv_full_path)

    def cleanup_empty_db(self, db_name):
        """
        Checks for an empty db and removes if so.
        """
        conn = sqlite3.connect(db_name)
        cur = conn.cursor()
        cur.execute('SELECT COUNT(*) from uploads;')
        record_count = cur.fetchone()[0]
        conn.close()

        if record_count == 0:
            print('\n\033[36mCleanup\n* The new uploads database contains ' +
                  'no records. Deleting it to reduce clutter.')
            os.remove(db_name)
        else:
            pass

    def print_db_name(self):
        """
        Prints name of the database.
        """
        print('\n\033[36mDatabase Name\n* Responses from the DocumentCloud ' +
              'API are stored in a SQLite database in your current ' +
              'directory at: ' + self.db_full_path)
