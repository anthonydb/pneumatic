Changelog
=========

0.1.9 - January 18, 2020
--------------------------

* Fix issue with authenticating API credentials via Requests. (`#20 <https://github.com/anthonydb/pneumatic/issues/20>`_)
* Disable multiprocessing for now. (`#21 <https://github.com/anthonydb/pneumatic/issues/21>`_)
* Confirm Python 3.8 support.

0.1.8 - September 23, 2018
--------------------------

* Improve command-line message content and formatting.
* Confirm Python 3.6 and 3.7 support.
* Expand number of unsupported filetypes to exclude from import list.
* Improve CSV output file name formatting.
* Documentation edits and updates.

0.1.7 - November 24, 2016
-------------------------

* Delete SQLite database if, upon program exit, it contains no records. (`#14 <https://github.com/anthonydb/pneumatic/issues/14>`_)
* Add some color, improve readability in console output. (`#18 <https://github.com/anthonydb/pneumatic/issues/18>`_)
* Add colorama dependency for printing ANSI escape code colors in Windows.

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
