Database Features
==================

Each time you start an upload, pneumatic creates a table called ``uploads`` in a SQLite database that captures the following local file data plus data from DocumentCloud's API response:

* ``file_name``: Name of the file submitted for upload.
* ``full_path``: The full directory path to the file, including the file name.
* ``upload_time``: Timestamp indicating the time of upload.
* ``result``: HTTP response code from DocumentCloud. ``200`` indicates success.
* ``canonical_url``: The URL to the document displayed in the viewer on DocumentCloud.
* ``pdf_url``: The URL to the PDF.
* ``text_url``: The URL to the extracted text of the document.
* ``exclude_flag``: Flag indicating whether pneumatic excluded the file from being uploaded. For information on why files might be excluded, see the documentation on File Exclusions.
* ``exclude_reason``: The reason a file was excluded from upload.
* ``error_msg``: Server error message if upload attempt failed.

Printing the database name and location
---------------------------------------

After you initiate a ``DocumentCloudUploader`` object and begin the upload, you can instruct pneumatic to print the path to and name of the database file:

.. code-block:: python

    uploader.db.print_db_name()


Viewing database contents
-------------------------

There are number of tools available for viewing and querying the SQLite database's contents. One example that's simple to use is the `SQLite Manager <https://addons.mozilla.org/en-US/firefox/addon/sqlite-manager/>`_ browser plugin for Firefox.

pneumatic also provides a method to dump the database to a CSV file, which you can then load into Excel or other application. If you choose to do so in the same script where you have initiated an upload client, use the following:

.. code-block:: python

    uploader.db.dump_to_csv()

If you're coming back to an old database, or you forgot to dump the CSV while the object was alive, you can still dump to a CSV by importing a ``Database()`` object:

.. code-block:: python

    from pneumatic import Database

    db = Database()
    db.dump_to_csv('path/to/file.db')




