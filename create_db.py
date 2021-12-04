#!/usr/bin/env python
#-----------------------------------------------------------------------
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

def db_connect():
    # Connect to database created with direct server connection
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="wolson@Dev",
    database ="energydb"
    )
    mycursor = mydb.cursor(buffered=True)
    stmt_str = "CREATE TABLE curr_fhinfo("
    stmt_str += "fh_id VARCHAR(5), "
    stmt_str += "energy_consumption DECIMAL(10, 3), "
    stmt_str += "lab_id VARCHAR(10), "
    stmt_str += "PRIMARY KEY(fh_id));"
    mycursor.execute(stmt_str)
    stmt_str = "CREATE TABLE curr_labinfo("
    stmt_str += "lab_id VARCHAR(5), "
    stmt_str += "energy_consumption DECIMAL(10, 3), "
    stmt_str += "fh_opens VARCHAR(30), "
    stmt_str += "occupants INTEGER(3), "
    stmt_str += "avg_consumption DECIMAL(10, 3), "
    stmt_str += "energy_change VARCHAR(10), "
    stmt_str += "temperature VARCHAR(30), "
    stmt_str += "PRIMARY KEY(lab_id));"
    mycursor.execute(stmt_str)
    stmt_str = "CREATE TABLE day_fhinfo("
    stmt_str += "fh_id VARCHAR(5), "
    stmt_str += "total_consumption DECIMAL(10, 3), " #append to this with the curr data
    stmt_str += "lab_id VARCHAR(10), "
    stmt_str += "PRIMARY KEY(fh_id));"
    mycursor.execute(stmt_str)
    stmt_str = "CREATE TABLE day_labinfo("
    stmt_str += "lab_id VARCHAR(5), "
    stmt_str += "fh_ids VARCHAR(30), " #string list of fh ids
    stmt_str += "total_consumption DECIMAL(10, 3), "
    stmt_str += "lab_id VARCHAR(10), "
    stmt_str += "PRIMARY KEY(lab_id));"
    mycursor.execute(stmt_str)
    stmt_str = "CREATE TABLE week_fhinfo("
    stmt_str += "fh_id VARCHAR(5), "
    stmt_str += "total_consumption DECIMAL(10, 3), " #append to this with the curr data
    stmt_str += "lab_id VARCHAR(10), "
    stmt_str += "PRIMARY KEY(fh_id));"
    mycursor.execute(stmt_str)
    stmt_str = "CREATE TABLE week_labinfo("
    stmt_str += "lab_id VARCHAR(5), "
    stmt_str += "fh_ids VARCHAR(30), " #string list of fh ids
    stmt_str += "total_consumption DECIMAL(10, 3), "
    stmt_str += "lab_id VARCHAR(10), "
    stmt_str += "PRIMARY KEY(lab_id));"
    mycursor.execute(stmt_str)
    stmt_str = "CREATE TABLE month_fhinfo("
    stmt_str += "fh_id VARCHAR(5), "
    stmt_str += "total_consumption DECIMAL(10, 3), " #append to this with the curr data
    stmt_str += "lab_id VARCHAR(10), "
    stmt_str += "PRIMARY KEY(fh_id));"
    mycursor.execute(stmt_str)
    stmt_str = "CREATE TABLE month_labinfo("
    stmt_str += "lab_id VARCHAR(5), "
    stmt_str += "fh_ids VARCHAR(30), " #string list of fh ids
    stmt_str += "total_consumption DECIMAL(10, 3), "
    stmt_str += "lab_id VARCHAR(10), "
    stmt_str += "PRIMARY KEY(lab_id));"
    mycursor.execute(stmt_str)
    stmt_str = "CREATE TABLE year_fhinfo("
    stmt_str += "fh_id VARCHAR(5), "
    stmt_str += "total_consumption DECIMAL(10, 3), " #append to this with the curr data
    stmt_str += "lab_id VARCHAR(10), "
    stmt_str += "PRIMARY KEY(fh_id));"
    mycursor.execute(stmt_str)
    stmt_str = "CREATE TABLE year_labinfo("
    stmt_str += "lab_id VARCHAR(5), "
    stmt_str += "fh_ids VARCHAR(30), " #string list of fh ids
    stmt_str += "total_consumption DECIMAL(10, 3), "
    stmt_str += "lab_id VARCHAR(10), "
    stmt_str += "PRIMARY KEY(lab_id));"
    mydb.commit()
    print('success')
    # mycursor = mydb.cursor(buffered=True)
    # stmt_str = "SHOW TABLES"
    # print(mycursor.fetchall())
#---------------------------------------------------------
if __name__ == '__main__':
    db_connect()
