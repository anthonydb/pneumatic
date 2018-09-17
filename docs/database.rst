Database Features
==================

Each time you start an upload, pneumatic creates a table called ``uploads`` in a SQLite database in a folder called ``pneumatic_db`` in the current directory. The ``uploads`` table captures the following local file data plus data from DocumentCloud's API response:

* ``id``: The unique document id stored by DocumentCloud. Typically, it's in the form of a number followed by several words. e.g. ``12345-some-document-title``.
* ``title``: The document's title.
* ``file_name``: Name of the file submitted for upload.
* ``full_path``: The full directory path to the file, including the file name.
* ``upload_time``: Timestamp indicating the time of upload.
* ``pages``: The number of pages in the document.
* ``file_hash``: A unique identifier calculated based on the document. Useful for finding identical documents.
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

There are number of tools available for viewing and querying the SQLite database's contents. One example that's simple to use is the `DB Browser for SQLite <http://sqlitebrowser.org/>`_ GUI app, available for Windows and macOS. If you prefer to work from the command line, see the `SQLite command line app <https://sqlite.org/cli.html>`_ documentation.

pneumatic also provides a method to dump the database to a CSV file, which you can then load into Excel or other applications. If you choose to do so in the same script where you have initiated an upload client, use the following:

.. code-block:: python

    uploader.db.dump_to_csv()

If you're coming back to an old database, or you forgot to dump the CSV while the object was alive, you can still dump to a CSV by importing a ``Database()`` object:

.. code-block:: python

    from pneumatic import Database

    db = Database()
    db.dump_to_csv('path/to/file.db')

Updating database contents
--------------------------

The API response to a DocumentCloud upload does not include an actual value for ``pages`` or ``file_hash``. These are calculated as part of DocumentCloud's processing of the document. Once your documents are finished processing, you can use pneumatic to go back and retrieve those values with the ``update_processed_files`` method.

You can use the method within a current session, which will update the database active in the session, or you can pass in the name of any other database file pneumatic created.

To use within the current session:

.. code-block:: python

    uploader.update_processed_files()

To come back to an older database and process it:

.. code-block:: python

    from pneumatic import DocumentCloudUploader

    uploader = DocumentCloudUploader('person@example.com', 'your-password')
    uploader.update_processed_files('path/to/file.db')

Currently, only ``title``, ``pages`` and ``file_hash`` are updated.

