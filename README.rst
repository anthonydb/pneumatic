Pneumatic: A Bulk-Upload Library for DocumentCloud
==================================================

pneumatic is a library intended to add some luxury and safeguards to the process of bulk-uploading hundreds, thousands or hundreds of thousands of files to DocumentCloud. **Note: pneumatic is currently very much a work in progress.**

Features
--------

- Catalogs the API response for each upload in a SQLite database along with the file's canonical URL.
- Prevents inadvertent submission of files that DocumentCloud doesn't handle, such as audio.

Usage
-----

You will need to have an active DocumentCloud account. Your

.. code-block:: python

    from pneumatic import DocumentCloudUploader

    client = DocumentCloudUploader('person@example.com', 'your-password')
    client.upload(file_directory='/files', project='17477-loudoun-county-government')

