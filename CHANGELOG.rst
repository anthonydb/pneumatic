Changelog
=========

Development
-----------

* Add ``update_processed_files`` method to get page, file hash and other data that's not available upon upload.
* Add ``pages`, ``file_hash`, ``id`` and ``title`` to items tracked in database.
* Create database upon DocumentCloudUploader initialization.
* Bug fix: Properly test for presence of data and title keyword arguments.

0.1.4 - February 17, 2016
-------------------------

* Remove extra line space on csv dump in Windows.

0.1.3 - February 16, 2016
-------------------------

* Report number of files to be uploaded before starting.
* Better reporting of upload progress and results.
* More comprehensive filetype exclusion list.
* Record pdf and text URLs in database.
* Uploads that return status codes other than 200 are handled.

0.1.2 - February 4, 2016
------------------------

* ``dump_to_csv`` outputs contents of SQLite database.
* Add ``force_ocr`` parameter to upload options.
* Removed multiprocessing support for Windows for now.
* Report when upload file directory does not exist.
* Better testing for prohibited file types.
* Only create database after file path verified.

0.1.1 - December 31, 2015
-------------------------

* Packaged for release to PyPi.

0.1 - December 16, 2015
-----------------------

* Add multiprocessing. (#1)
* Exclude files of 400MB or larger from upload. (#3)
* Add initial tests.
* Scaffolding for documentation.

0.0.1 - November 26, 2015
-------------------------

* Pre-alpha prototype
