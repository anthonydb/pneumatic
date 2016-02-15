A Bulk-Upload Library for DocumentCloud
---------------------------------------

pneumatic is a Python 3 library that adds some luxury and safeguards to the bulk-uploading of hundreds, thousands or hundreds of thousands of files to `DocumentCloud <https://www.documentcloud.org>`_. It is meant to do one thing -- upload -- and serve as an adjunct to, but not a replacement for, the excellent `python-documentcloud <http://python-documentcloud.readthedocs.org/en/latest/>`_ API wrapper.

pneumatic's name is inspired by the pneumatic dispatch systems in newsrooms of yore, which featured a `series of pneumatic tubes`_ for sending copy from the newsrooms to other departments such as the composing room.

Features
--------

- Catalogs the API response for each upload in a SQLite database along with the file's canonical URL.
- Dumps the SQLite data to a CSV if you wish.
- Multiprocessing (under Mac/Linux) for faster submission of files to DocumentCloud's API.
- Prevents inadvertent submission of file types DocumentCloud doesn't handle, such as audio.

Links
-----

* Documentation:    https://pneumatic.readthedocs.org/
* Repository:       https://github.com/anthonydb/pneumatic
* Issues:           https://github.com/anthonydb/pneumatic/issues

Basic Usage
-----------

You will need an active DocumentCloud account. Example use: To upload all files in a directory (and all sub-directories below it), assign them to an existing project, set the files to public access, and tag each with metadata, run the following code:

.. code-block:: python

    from pneumatic import DocumentCloudUploader

    uploader = DocumentCloudUploader('person@example.com', 'your-password')
    uploader.upload(
        file_directory='/govfiles',
        project='17477-loudoun-county-government',
        access='public',
        data={'type': 'government', 'action': 'lawsuit'})

.. _`series of pneumatic tubes`: https://en.wikipedia.org/wiki/Pneumatic_tube
