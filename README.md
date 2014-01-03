nutch-hbase-reader
==================

This project provides a simple web interface to read the docinfo from hbase(fetch time, status, outlinks, etc. WebPage in nutch2.*).

Getting Started
============

    twisted -ny app.py

Now the server should be running on http://localhost:6800

The configuration in is config.py.
    
    HBASE_HOST = "" # hbase hostname
    HBASE_TABLE = "" # hbase tablename
    BIND_ADDRESS = "0.0.0.0" # the server you are in
    HTTP_PORT = 6800 # default server port

Requirements
============
* Python 2.*
* Twisted
