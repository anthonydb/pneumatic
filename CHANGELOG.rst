Changelog
=========

0.1.6 - April 28, 2016
----------------------

* Provide ``User-Agent`` and ``From`` HTTP header fields.
* Correct issue where ``force_ocr`` and ``secure`` parameters were not being set default to ``false`` in the Ruby way. (`#17 <https://github.com/anthonydb/pneumatic/issues/17>`_)
* Handle 50X errors from the API (which do not return JSON). (`#15 <https://github.com/anthonydb/pneumatic/issues/15>`_, thank you, `Tom Meagher <https://github.com/tommeagher>`_!)

0.1.5 - March 9, 2016
---------------------

* Add ``update_processed_files`` method to get page, file hash and other data that's not available upon upload.
* Add ``pages``, ``file_hash``, ``id`` and ``title`` to items tracked in database.
* Create database upon ``DocumentCloudUploader`` initialization.
* Get rid of the file extension in the document title. (`#13 <https://github.com/anthonydb/pneumatic/issues/13>`_)
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

* ``dump_to_csv`` outputs contents of SQLite database. (`#2 <https://github.com/anthonydb/pneumatic/issues/2>`_)
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

* Add multiprocessing. (`#1 <https://github.com/anthonydb/pneumatic/issues/1>`_)
* Exclude files of 400MB or larger from upload. (`#3 <https://github.com/anthonydb/pneumatic/issues/3>`_)
* Add initial tests.
* Scaffolding for documentation.

0.0.1 - November 26, 2015
-------------------------

* Pre-alpha prototype
