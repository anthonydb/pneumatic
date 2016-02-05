Uploading
=========

pneumatic is designed for one thing: uploading documents. It supports all parameters found in the `DocumentCloud API upload endpoint <https://www.documentcloud.org/help/api#upload-documents>`_.

Create a client
---------------

To create an upload client, import the ``DocumentCloudUploader`` class in your Python script and create a client object. You must have a valid DocumentCloud account. Supply your email and password as arguments:

.. code-block:: python

    from pneumatic import DocumentCloudUploader

    uploader = DocumentCloudUploader('person@example.com', 'your-password')

Start an upload
---------------

Use the ``upload`` method to upload files, passing in parameters as desired. For a complete list of available parameters, consult the `DocumentCloud API documentation <https://www.documentcloud.org/help/api#upload-documents>`_.

For example, after you import pneumatic and creat a client as shown above, you can initiate the upload with code such as this:

.. code-block:: python

    uploader.upload(
        file_directory='/govfiles',
        project='17477-loudoun-county-government',
        access='public',
        data={'type': 'government', 'action': 'lawsuit'})

In this example, pneumatic will attempt to upload all files in the ``/govfiles`` directory and all subdirectories below it. In addition, it will assign the files to an existing project (must have been created already), set each file to public access, and tag each file with custom metadata.

If no ``file_directory`` parameter is supplied, pneumatic uploads files in the directory from which you execute your Python script.

File exclusions
---------------

DocumentCloud accepts a variety of file types for upload. In addition to PDFs, users can submit Word and Excel files, PowerPoint, and a variety of images. pneumatic will not submit files that exceed DocumentCloud's 400MB size limit, nor will it submit file types that the platform does not handle, such as audio.

Upload results
--------------

DocumentCloud's API returns data for each file uploaded, and pneumatic catalogs key pieces of this data in a SQLite database that is automatically created under a ``pneumatic_db`` directory in the directory specified for uploads. See the database features documentation for additional information.

Multiprocessing support
-----------------------

If you are using a Mac or Linux computer, pneumatic uses the Python multiprocessing library to more rapidly submit files to the DocumentCloud API. Multiprocessing is not currently supported under Windows. Note that this speed improvement does not impact actual processing time for files on DocumentCloud.
