Use With python-documentcloud
=============================

pneumatic happily coexists with `python-documentcloud <http://python-documentcloud.readthedocs.org/en/latest/>`_, a full-featured wrapper for the `DocumentCloud API <https://www.documentcloud.org/help/api>`_. python-documentcloud offers extensive methods for interacting with documents, projects, annotations, entities and other aspects of the platform.

For example, you can create a project with python-documentcloud, then use pneumatic to upload files and capture the results data:

.. code-block:: python

    # Import both libraries.
    from pneumatic import DocumentCloudUploader
    from documentcloud import DocumentCloud

    # Create the respective clients.
    uploader = DocumentCloudUploader('person@example.com', 'your-password')
    dc_client = DocumentCloud('person@example.com', 'your-password')

    # Using python-documentcloud, create a project under your account.
    project = dc_client.projects.create('Loudoun Fire')

    # Using pneumatic, upload your files. Add them to the project id obtained when
    # the project was created just now.
    uploader.upload(
        file_directory='/path-to/files',
        project=project.id,
        source='Loudoun County Fire and Rescue',
        data={'topic': 'fires'})

    # pneumatic made a database of your upload results. Print its name and location.
    uploader.db.print_db_name()

    # Dump the pneumatic upload results data to a CSV.
    uploader.db.dump_to_csv()
