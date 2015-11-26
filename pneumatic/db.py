import os
import sqlite3
from utils import Utils


class Database(object):
    """
    A database to store results of file upload attempts to DocumentCloud.
    """

    def __init__(self):
        # Create a sqlite db whose name includes a timestamp.
        self.utils = Utils()
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
            cur.execute('''CREATE TABLE uploads
                (file_name Text, upload_time Text, result Text, canonical_url Text)
            ''')
            conn.commit()
            conn.close()
        else:
            pass

    def insert_row(self, file_name, up_time, result, canonical_url):
        """
        Inserts a row in the table.
        """
        conn = sqlite3.connect(self.db_full_path)
        cur = conn.cursor()
        cur.execute('''
            INSERT INTO uploads VALUES (?,?,?,?);
            ''', (file_name, up_time, result, canonical_url))
        conn.commit()
        conn.close()

    def print_db_name(self):
        """
        Prints name of the database.
        """
        print 'Upload data will be stored in ' + self.db_full_path
