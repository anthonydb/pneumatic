Pneumatic: Bulk-Uploading for DocumentCloud
==================================================

pneumatic is a library intended to add some luxury and safeguards to the bulk-uploading of hundreds, thousands or hundreds of thousands of files to `DocumentCloud <https://www.documentcloud.org`_. It is meant to serve as an adjunct to, but not a replacement for, the excellent `python-documentcloud <http://python-documentcloud.readthedocs.org/en/latest/>` API wrapper.

pneumatic's name is inspired by the newsrooms of yore, which featured a `series of pneumatic tubes`_ for sending copy from the newsrooms to the composing room and other locations.

Features
--------

- Multiprocessing for faster submission of files to DocumentCloud's API.
- Catalogs the API response for each upload in a SQLite database along with the file's canonical URL.
- Prevents inadvertent submission of files that DocumentCloud doesn't handle, such as audio.

Links
-----

* Documentation:    http://pneumatic.readthedocs.org/
* Repository:       https://github.com/anthonydb/pneumatic
* Issues:           https://github.com/anthonydb/pneumatic/issues

Basic Usage
-----------

You will need an active DocumentCloud account. Uploading all files in a directory (and all sub-directories below it), is as simple as running:

.. code-block:: python

    from pneumatic import DocumentCloudUploader

    client = DocumentCloudUploader('person@example.com', 'your-password')
    client.upload(file_directory='/files', project='17477-loudoun-county-government')


.. _`series of pneumatic tubes`: http://evolvingnewsroom.nz/wp-content/uploads/2008/10/newsroom-tubes1.jpg
