Uploading
=========

pneumatic supports all parameters found in the DocumentCloud upload API endpoint.

Create a client
---------------

To create an upload client, import the ``DocumentCloudUploader`` class in your Python script and create a client object. You must have a valid DocumentCloud account. Supply your email and password as arguments:

.. code-block:: python

    from pneumatic import DocumentCloudUploader

    client = DocumentCloudUploader('person@example.com', 'your-password')

Start an upload
---------------

Use the ``upload`` method to upload files, passing in parameters as desired.

