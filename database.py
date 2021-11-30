#!/usr/bin/env python
#-----------------------------------------------------------------------
# Authors: abc123
#-----------------------------------------------------------------------
from contextlib import closing
from random import randrange
from sys import argv, stderr
import sys
from datetime import date, timedelta
import pymysql

def put_fumehood_output(date, fh_id):
    # we will only ever post to the day table from here - all other updates will occur in cron/on cpanel
    '''get the average fumehood consumption for a given date'''
    conn = pymysql.connect(host='67.205.146.88',
                             user='labenergy',
                             password='lab_energy_monitoring_cos333',                             
                             db='labenerg_energydb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:  
        with conn.cursor() as cursor: 
            stmt_str = "INSERT INTO day_fhinfo (consumption) values (%s)"
            cursor.execute(stmt_str, fh_id)
    finally:
        # Close connection.
        conn.close()

# def put_fumehood_output(date, cursor, value):
def get_fumehood_output(tabletime, date, fh_id):
    # time range determines which table to query from 
    if tabletime == 'day':
        timerange = 'day_fhinfo'
    elif tabletime == 'week':
        timerange = 'week_fhinfo'
    elif tabletime == 'month':
        timerange = 'month_fhinfo'
    else:
        timerange = 'year_fhinfo'

    '''get the average fumehood consumption for a given date'''
    conn = pymysql.connect(host='67.205.146.88',
                             user='labenergy',
                             password='lab_energy_monitoring_cos333',                             
                             db='labenerg_energydb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:  
        with conn.cursor() as cursor: 
            stmt_str = "SELECT * FROM %s WHERE id=%s AND date=%s"
            cursor.execute(stmt_str, timerange, date, fh_id)
            if cursor.rowcount == 0: 
                return('ERROR: DATA FOR DATE ' +date+ ' NOT FOUND.')
            else:
                return(cursor.fetchone()) 
    finally:
        # Close connection.
        conn.close()

def put_lab_info(date, fh_id):
    # we will only ever post to the day table from here - all other updates will occur in cron/on cpanel
    '''get the average fumehood consumption for a given date'''
    conn = pymysql.connect(host='67.205.146.88',
                             user='labenergy',
                             password='lab_energy_monitoring_cos333',                             
                             db='labenerg_energydb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:  
        with conn.cursor() as cursor: 
            stmt_str = "INSERT INTO day_labinfo (consumption) values (%s)"
            cursor.execute(stmt_str, fh_id)
    finally:
        # Close connection.
        conn.close()

# def put_fumehood_output(date, cursor, value):
def get_lab_info(tabletime, date, fh_id):
    # time range determines which table to query from 
    if tabletime == 'day':
        timerange = 'day_labinfo'
    elif tabletime == 'week':
        timerange = 'week_labinfo'
    elif tabletime == 'month':
        timerange = 'month_labinfo'
    else:
        timerange = 'year_labinfo'

    '''get the average fumehood consumption for a given date'''
    conn = pymysql.connect(host='67.205.146.88',
                             user='labenergy',
                             password='lab_energy_monitoring_cos333',                             
                             db='labenerg_energydb',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)
    try:  
        with conn.cursor() as cursor: 
            stmt_str = "SELECT * FROM %s WHERE id=%s AND date=%s"
            cursor.execute(stmt_str, timerange, date, fh_id)
            if cursor.rowcount == 0: 
                return('ERROR: DATA FOR DATE ' +date+ ' NOT FOUND.')
            else:
                return(cursor.fetchone()) 
    finally:
        # Close connection.
        conn.close()

def main():
    get_fumehood_output(1,2)

    
#---------------------------------------------------------
if __name__ == '__main__':
    main()
