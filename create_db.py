#!/usr/bin/env python
#-----------------------------------------------------------------------
# create_db.py
# Authors: abc123
# Create a dummy database for energy values.
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
from lab_query import lab_info


def init_day_table(cursor):
    '''initialize day table to 0 to begin appending live data'''
    labs_fhs = {'rabinowitz_icahn_201':['fh5c', 'fh5d', 'fh6c', 'fh6d'],
    'rabinowitz_icahn_202':['fh7c', 'fh7d', 'fh8c', 'fh8d']}
    for lab in labs_fhs.keys():
        for fh in labs_fhs[lab]:
            fh_input = [str(fh),str(lab), 0.0, 0.0]
            stmt_str = "INSERT INTO day_fhinfo(fh_id, lab_id, energy_consumption, hours_open) "
            stmt_str += "VALUES(%s, %s, %s, %s);"
            cursor.execute(stmt_str,fh_input)
        lab_input = [str(lab), 0.0, 0.0, 0.0]
        stmt_str = "INSERT INTO day_labinfo(lab_id, fh_consumption, fh_opens, avg_consumption) "
        stmt_str += "VALUES(%s, %s, %s, %s);"
        cursor.execute(stmt_str,lab_input)

def create_db(cursor):
    stmt_str = "CREATE TABLE curr_fhinfo("
    stmt_str += "fh_id VARCHAR(50), "
    stmt_str += "is_open VARCHAR(5), "
    stmt_str += "energy_consumption VARCHAR(1000), "
    stmt_str += "lab_id VARCHAR(50), "
    stmt_str += "PRIMARY KEY(fh_id));"
    cursor.execute(stmt_str)
    stmt_str = "CREATE TABLE curr_labinfo("
    stmt_str += "lab_id VARCHAR(50), "
    stmt_str += "fh_consumption DECIMAL(10, 3), "
    stmt_str += "fh_opens VARCHAR(30), "
    stmt_str += "consumption DECIMAL(10, 3), "
    stmt_str += "PRIMARY KEY(lab_id));"
    cursor.execute(stmt_str)
    stmt_str = "CREATE TABLE day_fhinfo("
    stmt_str += "fh_id VARCHAR(50), "
    stmt_str += "lab_id VARCHAR(50), "
    stmt_str += "energy_consumption DECIMAL(10, 3), " #append to this with the curr data
    stmt_str += "hours_open INTEGER(5), " #append to this with the curr data
    stmt_str += "PRIMARY KEY(fh_id));"
    cursor.execute(stmt_str)
    stmt_str = "CREATE TABLE day_labinfo(" 
    stmt_str += "lab_id VARCHAR(50), "
    stmt_str += "fh_consumption DECIMAL(10, 3), "
    stmt_str += "fh_opens VARCHAR(30), "
    stmt_str += "avg_consumption DECIMAL(10, 3), "
    stmt_str += "PRIMARY KEY(lab_id));"
    cursor.execute(stmt_str)
    stmt_str = "CREATE TABLE week_fhinfo("
    stmt_str += "id VARCHAR(50), "
    stmt_str += "fh_id VARCHAR(50), "
    stmt_str += "lab_id VARCHAR(50), "
    stmt_str += "day VARCHAR(10), " # dummy 0-6, map to real
    stmt_str += "energy_consumption DECIMAL(10, 3), "
    stmt_str += "hours_open INTEGER(2), "
    stmt_str += "PRIMARY KEY(fh_id));"
    cursor.execute(stmt_str)
    stmt_str = "CREATE TABLE week_labinfo("
    stmt_str += "id VARCHAR(50), "
    stmt_str += "lab_id VARCHAR(50), "
    stmt_str += "day VARCHAR(10), " # dummy 0-6, map to real
    stmt_str += "fh_consumption DECIMAL(10, 3), "
    stmt_str += "fh_opens VARCHAR(30), "
    stmt_str += "avg_consumption DECIMAL(10, 3), "
    stmt_str += "PRIMARY KEY(lab_id));"
    cursor.execute(stmt_str)
    stmt_str = "CREATE TABLE month_fhinfo("
    stmt_str += "id VARCHAR(50), "
    stmt_str += "fh_id VARCHAR(50), "
    stmt_str += "lab_id VARCHAR(50), "
    stmt_str += "day VARCHAR(10), " # dummy 0-4, map to real
    stmt_str += "energy_consumption DECIMAL(10, 3), " 
    stmt_str += "hours_open INTEGER(2), "
    stmt_str += "PRIMARY KEY(fh_id));"
    cursor.execute(stmt_str)
    stmt_str = "CREATE TABLE month_labinfo("
    stmt_str += "id VARCHAR(50), "
    stmt_str += "lab_id VARCHAR(50), "
    stmt_str += "week VARCHAR(10), " # dummy 0-4, map to real
    stmt_str += "fh_consumption DECIMAL(10, 3), "
    stmt_str += "fh_opens VARCHAR(30), "
    stmt_str += "avg_consumption DECIMAL(10, 3), "
    stmt_str += "PRIMARY KEY(lab_id));"
    cursor.execute(stmt_str)
    stmt_str = "CREATE TABLE year_fhinfo("
    stmt_str += "id VARCHAR(50), "
    stmt_str += "fh_id VARCHAR(50), "
    stmt_str += "lab_id VARCHAR(50), "
    stmt_str += "month VARCHAR(10), " # dummy 0-11, map to real
    stmt_str += "energy_consumption DECIMAL(10, 3), "
    stmt_str += "hours_open INTEGER(2), "
    stmt_str += "PRIMARY KEY(fh_id));"
    cursor.execute(stmt_str)
    stmt_str = "CREATE TABLE year_labinfo("
    stmt_str += "id VARCHAR(50), "
    stmt_str += "lab_id VARCHAR(50), "
    stmt_str += "month VARCHAR(10), " # dummy 0-11, map to real
    stmt_str += "fh_consumption DECIMAL(10, 3), "
    stmt_str += "fh_opens VARCHAR(30), "
    stmt_str += "avg_consumption DECIMAL(10, 3), "
    stmt_str += "PRIMARY KEY(lab_id));"
    cursor.execute(stmt_str)
    init_day_table(cursor)

def main():
    # Connect to database created with direct server connection
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="wolson@Dev",
    database ="energydb")
    cursor = mydb.cursor(buffered=True)
    create_db(cursor)
    mydb.commit()
    print('success')
#---------------------------------------------------------
if __name__ == '__main__':
    main()
