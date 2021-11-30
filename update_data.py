#!/usr/bin/env python
"""dump table, take in list, add list fields to table"""
#-----------------------------------------------------------------------
# update_data.py
# Authors: abc123
#-----------------------------------------------------------------------
import sys
from sys import argv, stderr
from contextlib import closing
import sqlite3 as sq
from sqlite3 import connect

DATABASE_URL = 'something.mysql?mode=rwb'

def update(cursor):
    # dump table into dump.sql file
    dump_str = 'mysqldump --all-databases > dump.sql'
    cursor.execute(dump_str)


def main():
    """establish connection to database and parse args"""
    try:
        with connect(DATABASE_URL, uri = True) as connection:
            with closing(connection.cursor()) as cursor:
                update(cursor)
    except sq.Error as ex:
        print("sys.argv[0]: " +str(ex), file=stderr)
        sys.exit(1)

#------------------------------------------------------------------------------------
if __name__ == '__main__':
    main()