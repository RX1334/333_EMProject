#!/usr/bin/env python
#-----------------------------------------------------------------------
# pull_db.py
# Authors: Will Olson
# Query lab and fumehood data from MySQL database.
#-----------------------------------------------------------------------
from contextlib import closing
from random import randrange
from sys import argv, stderr
import sys
from datetime import date, timedelta
from typing import ItemsView
import mysql.connector
import random
from lab_query import lab_info

def pull_lab_data(time, lab, index):
    '''pull data from historical table'''
    # Connect to database created with direct server connection
    try:
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="wolson@Dev",
        database ="energydb")
    except Exception as ex:
        print("Server error.", ex)
    cursor = mydb.cursor(buffered=True)
    if time == 'daily':
        stmt_str = "SELECT fh_consumption, climate_consumption, total_consumption FROM daily_labinfo WHERE lab_id = "
        stmt_str += "%s AND day = %s;"
    elif time == 'weekly':
        stmt_str = "SELECT fh_consumption, climate_consumption, total_consumption FROM weekly_labinfo WHERE lab_id = "
        stmt_str += "%s AND week = %s;"
    elif time == 'monthly':
        stmt_str = "SELECT fh_consumption, climate_consumption, total_consumption FROM monthly_labinfo WHERE lab_id = "
        stmt_str += "%s AND month = %s;"
    elif time == 'yearly':
        stmt_str = "SELECT fh_consumption, climate_consumption, total_consumption FROM yearly_labinfo WHERE lab_id = "
        stmt_str += "%s AND year = %s;"
    else:
        return('Invalid Query')
    input = [lab, index]
    cursor.execute(stmt_str, input)
    out = cursor.fetchall()[0]
    mydb.commit()
    return{'fh': float(out[0]), 'climate': float(out[1]), 'total':float(out[2])}

def pull_fh_data(time, lab, fh, index):
    '''pull data from historical table'''
    try:
        mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="wolson@Dev",
        database ="energydb")
    except Exception as ex:
        print("Server error.", ex)
    cursor = mydb.cursor(buffered=True)
    if time == 'daily':
        stmt_str = "SELECT energy_consumption, hours_open FROM daily_fhinfo WHERE lab_id = "
        stmt_str += "%s AND fh_id = %s AND day = %s;"
    elif time == 'weekly':
        stmt_str = "SELECT energy_consumption, hours_open FROM weekly_fhinfo WHERE lab_id = "
        stmt_str += "%s AND fh_id = %s AND week = %s;"
    elif time == 'monthly':
        stmt_str = "SELECT energy_consumption, hours_open FROM monthly_fhinfo WHERE lab_id = "
        stmt_str += "%s AND fh_id = %s AND month = %s;"
    elif time == 'yearly':
        stmt_str = "SELECT energy_consumption, hours_open FROM yearly_fhinfo WHERE lab_id = "
        stmt_str += "%s AND fh_id = %s AND year = %s;"
    else:
        return('Invalid Query')
    input = [lab, fh, index]
    cursor.execute(stmt_str, input)
    mydb.commit()
    out = cursor.fetchall()[0]
    return{'energy': float(out[0]), 'hours':float(out[1])}

def main():
    print(pull_lab_data('daily', 'rabinowitz_icahn_201', 1))
    print(pull_lab_data('weekly', 'rabinowitz_icahn_201', 1))
    print(pull_lab_data('monthly', 'rabinowitz_icahn_201', 1))
    print(pull_lab_data('yearly', 'rabinowitz_icahn_201', 1))
    print(pull_lab_data('daily', 'rabinowitz_icahn_201', 1))
    print(pull_fh_data('weekly', 'rabinowitz_icahn_201', 'fh5c', 1))
    print(pull_fh_data('monthly', 'rabinowitz_icahn_202', 'fh7c', 1))
    print(pull_fh_data('yearly', 'rabinowitz_icahn_201', 'fh6c', 1))
#---------------------------------------------------------
if __name__ == '__main__':
    main()
