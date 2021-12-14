#!/usr/bin/env python
#-----------------------------------------------------------------------
# push_db.py
# Authors: Lab Energy Monitoring Team
# Connect and make queries to the MySQL DB.
#-----------------------------------------------------------------------
from contextlib import closing
from random import randrange
from sys import argv, stderr
import sys
from datetime import date, timedelta
import mysql.connector
import random

def put_lab_db(lab, fh, climate, total):
    '''append instantaneous data to daily total table'''
    # Connect to database created with direct server connection
    try:
        mydb = mysql.connector.connect(
        host="energymonitor.princeton.edu",
        user="labenerg_wolson",
        password="lab_energy_monitoring_cos333",
        database ="labenerg_EMDatabase")
    except Exception as ex:
        print("Server error.", ex)
        # TEMPORARY RETURN FOR LOCAL TESTING
        return
    cursor = mydb.cursor(buffered=True)
    stmt_str = "SELECT fh_consumption, climate_consumption, total_consumption FROM today_labinfo WHERE lab_id = "
    stmt_str += "%s;"
    cursor.execute(stmt_str, [lab])
    data = cursor.fetchall()[0]
    fumehood = float(data[0])
    clim = float(data[1])
    tot = float(data[2])
    fumehood += fh
    clim += climate
    tot += total
    values = [lab, str(fumehood), str(clim), str(tot)]
    stmt_str = "REPLACE INTO today_labinfo(lab_id, fh_consumption, climate_consumption, total_consumption) "
    stmt_str += "VALUES(%s, %s, %s, %s);"
    cursor.execute(stmt_str, values)
    mydb.commit()

def put_fh_db(fh, lab, nrg, hr):
    '''append instantaneous data to daily total table'''
    # Connect to database created with direct server connection
    try:
        mydb = mysql.connector.connect(
        host="energymonitor.princeton.edu",
        user="labenerg_wolson",
        password="lab_energy_monitoring_cos333",
        database ="labenerg_EMDatabase")
    except Exception as ex:
        print("Server error.", ex)
        # TEMPORARY RETURN FOR LOCAL TESTING, DELETE LATER
        return
    cursor = mydb.cursor(buffered=True)
    stmt_str = "SELECT energy_consumption, hours_open FROM today_fhinfo WHERE fh_id = "
    stmt_str += "%s;"
    cursor.execute(stmt_str, [fh])
    data = cursor.fetchall()[0]
    energy = float(data[0])
    hour = float(data[1]/60/60) # convert to fraction of an hour
    energy += nrg
    hour += hr
    values = [fh, lab, str(energy), str(hour)]
    stmt_str = "REPLACE INTO today_fhinfo(fh_id, lab_id, energy_consumption, hours_open) "
    stmt_str += "VALUES(%s, %s, %s, %s);"
    cursor.execute(stmt_str, values)
    mydb.commit()

def main():
    put_fh_db('fh5c', 'rabinowitz_icahn_201', .08, 1)
    put_lab_db('rabinowitz_icahn_201', .08, 2, 3)
#---------------------------------------------------------
if __name__ == '__main__':
    main()
