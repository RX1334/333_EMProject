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
            stmt_str = "INSERT INTO today_fhinfo(fh_id, lab_id, energy_consumption, hours_open) "
            stmt_str += "VALUES(%s, %s, %s, %s);"
            cursor.execute(stmt_str,fh_input)
        lab_input = [str(lab), 0.0, 0.0, 0.0]
        stmt_str = "INSERT INTO today_labinfo(lab_id, fh_consumption, climate_consumption, total_consumption) "
        stmt_str += "VALUES(%s, %s, %s, %s);"
        cursor.execute(stmt_str,lab_input)

def create_db(cursor):
    stmt_str = "CREATE TABLE today_fhinfo("
    stmt_str += "fh_id VARCHAR(50), "
    stmt_str += "lab_id VARCHAR(50), "
    stmt_str += "energy_consumption DECIMAL(10, 3), "
    stmt_str += "hours_open DECIMAL(10, 3), "
    stmt_str += "PRIMARY KEY(fh_id));"
    cursor.execute(stmt_str)
    stmt_str = "CREATE TABLE today_labinfo(" 
    stmt_str += "lab_id VARCHAR(50), "
    stmt_str += "fh_consumption DECIMAL(10, 3), "
    stmt_str += "climate_consumption DECIMAL(10,3), "
    stmt_str += "total_consumption DECIMAL(10, 3), "
    stmt_str += "PRIMARY KEY(lab_id));"
    cursor.execute(stmt_str)
    stmt_str = "CREATE TABLE daily_fhinfo("
    stmt_str += "id VARCHAR(50), "
    stmt_str += "fh_id VARCHAR(50), "
    stmt_str += "lab_id VARCHAR(50), "
    stmt_str += "day VARCHAR(50), " # dummy 0-5, map to real
    stmt_str += "energy_consumption DECIMAL(10, 3), "
    stmt_str += "hours_open DECIMAL(10,3), "
    stmt_str += "PRIMARY KEY(id));"
    cursor.execute(stmt_str)
    stmt_str = "CREATE TABLE daily_labinfo("
    stmt_str += "id VARCHAR(50), "
    stmt_str += "lab_id VARCHAR(50), "
    stmt_str += "day VARCHAR(50), " # dummy 0-5, map to real
    stmt_str += "fh_consumption DECIMAL(10, 3), "
    stmt_str += "climate_consumption DECIMAL(10,3), "
    stmt_str += "total_consumption DECIMAL(10, 3), "
    stmt_str += "PRIMARY KEY(id));"
    cursor.execute(stmt_str)
    stmt_str = "CREATE TABLE weekly_fhinfo("
    stmt_str += "id VARCHAR(50), "
    stmt_str += "fh_id VARCHAR(50), "
    stmt_str += "lab_id VARCHAR(50), "
    stmt_str += "week VARCHAR(50), " # dummy 0-3, map to real
    stmt_str += "energy_consumption DECIMAL(10, 3), "
    stmt_str += "hours_open DECIMAL(10,3), "
    stmt_str += "PRIMARY KEY(id));"
    cursor.execute(stmt_str)
    stmt_str = "CREATE TABLE weekly_labinfo("
    stmt_str += "id VARCHAR(50), "
    stmt_str += "lab_id VARCHAR(50), "
    stmt_str += "week VARCHAR(50), " # dummy 0-3, map to real
    stmt_str += "fh_consumption DECIMAL(10, 3), "
    stmt_str += "climate_consumption DECIMAL(10,3), "
    stmt_str += "total_consumption DECIMAL(10, 3), "
    stmt_str += "PRIMARY KEY(id));"
    cursor.execute(stmt_str)
    stmt_str = "CREATE TABLE monthly_fhinfo("
    stmt_str += "id VARCHAR(50), "
    stmt_str += "fh_id VARCHAR(50), "
    stmt_str += "lab_id VARCHAR(50), "
    stmt_str += "month VARCHAR(50), " # dummy 0-11, map to real
    stmt_str += "energy_consumption DECIMAL(10, 3), " 
    stmt_str += "hours_open DECIMAL(10, 3), "
    stmt_str += "PRIMARY KEY(id));"
    cursor.execute(stmt_str)
    stmt_str = "CREATE TABLE monthly_labinfo("
    stmt_str += "id VARCHAR(50), "
    stmt_str += "lab_id VARCHAR(50), "
    stmt_str += "month VARCHAR(50), " # dummy 0-11, map to real
    stmt_str += "fh_consumption DECIMAL(10, 3), "
    stmt_str += "climate_consumption DECIMAL(10,3), "
    stmt_str += "total_consumption DECIMAL(10, 3), "
    stmt_str += "PRIMARY KEY(id));"
    cursor.execute(stmt_str)
    stmt_str = "CREATE TABLE yearly_fhinfo("
    stmt_str += "id VARCHAR(50), "
    stmt_str += "fh_id VARCHAR(50), "
    stmt_str += "lab_id VARCHAR(50), "
    stmt_str += "year VARCHAR(50), " # dummy 0-4, map to real
    stmt_str += "energy_consumption DECIMAL(10, 3), "
    stmt_str += "hours_open DECIMAL(10, 3), "
    stmt_str += "PRIMARY KEY(id));"
    cursor.execute(stmt_str)
    stmt_str = "CREATE TABLE yearly_labinfo("
    stmt_str += "id VARCHAR(50), "
    stmt_str += "lab_id VARCHAR(50), "
    stmt_str += "year VARCHAR(50), " # dummy 0-4, map to real
    stmt_str += "fh_consumption DECIMAL(10, 3), "
    stmt_str += "climate_consumption DECIMAL(10,3), "
    stmt_str += "total_consumption DECIMAL(10, 3), "
    stmt_str += "PRIMARY KEY(id));"
    cursor.execute(stmt_str)
    init_day_table(cursor)

def main():
    try:
    # Connect to database created with direct server connection
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="wolson@Dev",
        database ="energydb")
        cursor = mydb.cursor(buffered=True)
        create_db(cursor)
        mydb.commit()
    except Exception as ex:
        print(ex, stderr)
#---------------------------------------------------------
if __name__ == '__main__':
    main()
