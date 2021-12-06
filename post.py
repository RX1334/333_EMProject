#!/usr/bin/env python
#-----------------------------------------------------------------------
# populate_db.py
# Authors: abc123
# Populate a dummy database for energy values.
# Values are randomized but follow approx.
# the same distribution as observed when connected
# to the REST API (ie the real values)
#-----------------------------------------------------------------------
from contextlib import closing
from random import randrange
from sys import argv, stderr
import sys
from datetime import date, timedelta
import mysql.connector
import random
from lab_query import lab_info

def post_to_db(fh, lab, curr_value):
    # Connect to database created with direct server connection
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="wolson@Dev",
    database ="energydb")
    cursor = mydb.cursor(buffered=True)
    stmt_str = "SELECT energy_consumption FROM curr_fhinfo WHERE fh_id = "
    stmt_str += "'fh5c';"
    cursor.execute(stmt_str)
    value = float(cursor.fetchone()[0])
    value += float(curr_value)
    values = [fh, lab, str(value)]
    stmt_str = "REPLACE INTO day_fhinfo(fh_id, lab_id, energy_consumption) "
    stmt_str += "VALUES(%s, %s, %s);"
    cursor.execute(stmt_str, values)
    mydb.commit()
    print('success')

def main():
    post_to_db('fh5c', 'rabinowitz_icahn_201', .05)
#---------------------------------------------------------
if __name__ == '__main__':
    main()
