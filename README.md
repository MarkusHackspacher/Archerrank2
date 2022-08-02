Archerank2
==========

[![Build Status](https://app.travis-ci.com/MarkusHackspacher/Archerrank2.svg?branch=master)](https://travis-ci.org/MarkusHackspacher/Archerrank2)
[![Crowdin](https://d322cqt584bo4o.cloudfront.net/archerrank2/localized.svg)](https://crowdin.com/project/archerrank2)

For the evaluation of archery tournaments.

motivation
----------

I got a sqlite file from Archerank, but I did not receive the program itself.
Would like to create a program with which a better database,
and should create winners deeds as a pdf.

But data from Archerank2 should not use for Archerank,
because I have no software to test it and I would like it not.
Archerank2 should be a software with new ideas, modern design and free use (GPL). 
Help is very welcome.

install
-------

Clone from Github

```bash
git clone https://github.com/MarkusHackspacher/Archerrank2.git
```

Download and install Python 3.6 or higher from www.python.org

Install pyqt5 and sqlalchemy

```bash
pip3 install -r requirements.txt
```

Start with

Linux

```bash
./archerrank2.py
```

Windows

```commandline
python archerrank2.py
```

Usage
-----

```bash
usage: archerrank2.py [-h] [-db DATABASE] [-l LANGUAGE] [-log {1,2,3,4,5}]

optional arguments:
  -h, --help            show this help message and exit
  -db DATABASE, --database DATABASE
                        file of the database
  -l LANGUAGE, --language LANGUAGE
                        ISO code of language, de for Germany
  -log {1,2,3,4,5}      logging level
```
