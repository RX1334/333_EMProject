#!/usr/bin/env python
#-----------------------------------------------------------------------
# pull_db.py
# Authors: Lab Energy Monitoring Team
# Query lab and fumehood data from MySQL database.
#-----------------------------------------------------------------------
from contextlib import closing
from random import randrange
from sys import argv, stderr
import sys
from datetime import date, timedelta
import mysql.connector
import random

def week_report(lab_name, week):
    '''queries and generates weekly report'''
    try:
        mydb = mysql.connector.connect(
        host="energymonitor.princeton.edu",
        user="labenerg_wolson",
        password="lab_energy_monitoring_cos333",
        database ="labenerg_EMDatabase")
    except Exception as ex:
        print("Server error.", ex)
    cursor = mydb.cursor(buffered=True)
    stmt_str = "SELECT fh_consumption, climate_consumption, total_consumption FROM weekly_labinfo WHERE lab_id = "
    stmt_str += "%s AND week = 0;"
    input = [lab_name]
    cursor.execute(stmt_str, input)
    out = cursor.fetchall()[0]
    mydb.commit()
    return([float(i) for i in out])


def pull_lab_data(time, lab):
    '''pull data from historical table'''
    # Connect to database created with direct server connection
    try:
        mydb = mysql.connector.connect(
        host="energymonitor.princeton.edu",
        user="labenerg_wolson",
        password="lab_energy_monitoring_cos333",
        database ="labenerg_EMDatabase")
    except Exception as ex:
        print("Server error.", ex)
    cursor = mydb.cursor(buffered=True)
    if time == 'daily':
        stmt_str = "SELECT fh_consumption, climate_consumption, total_consumption FROM daily_labinfo WHERE lab_id = "
        stmt_str += "%s;"
    elif time == 'weekly':
        stmt_str = "SELECT fh_consumption, climate_consumption, total_consumption FROM weekly_labinfo WHERE lab_id = "
        stmt_str += "%s;"
    elif time == 'monthly':
        stmt_str = "SELECT fh_consumption, climate_consumption, total_consumption FROM monthly_labinfo WHERE lab_id = "
        stmt_str += "%s;"
    elif time == 'yearly':
        stmt_str = "SELECT fh_consumption, climate_consumption, total_consumption FROM yearly_labinfo WHERE lab_id = "
        stmt_str += "%s;"
    else:
        return('Invalid Query')
    input = [lab]
    cursor.execute(stmt_str, input)
    out = cursor.fetchall()
    output = {'fh': [], 'climate': [], 'total':[]}
    for i in out:
        output['fh'].append(float(i[0]))
        output['climate'].append(float(i[1]))
        output['total'].append(float(i[2]))
    mydb.commit()
    return(output)

def pull_fh_data(time, lab, fh):
    '''pull data from historical table'''
    try:
        mydb = mysql.connector.connect(
        host="energymonitor.princeton.edu",
        user="labenerg_wolson",
        password="lab_energy_monitoring_cos333",
        database ="labenerg_EMDatabase")
    except Exception as ex:
        print("Server error.", ex)
    cursor = mydb.cursor(buffered=True)
    if time == 'daily':
        stmt_str = "SELECT energy_consumption, hours_open FROM daily_fhinfo WHERE lab_id = "
        stmt_str += "%s AND fh_id = %s;"
    elif time == 'weekly':
        stmt_str = "SELECT energy_consumption, hours_open FROM weekly_fhinfo WHERE lab_id = "
        stmt_str += "%s AND fh_id = %s;"
    elif time == 'monthly':
        stmt_str = "SELECT energy_consumption, hours_open FROM monthly_fhinfo WHERE lab_id = "
        stmt_str += "%s AND fh_id = %s;"
    elif time == 'yearly':
        stmt_str = "SELECT energy_consumption, hours_open FROM yearly_fhinfo WHERE lab_id = "
        stmt_str += "%s AND fh_id = %s;"
    else:
        return('Invalid Query')
    input = [lab, fh]
    cursor.execute(stmt_str, input)
    mydb.commit()
    out = cursor.fetchall()
    output = {'energy':[], 'hours':[]}
    for i in out:
        output['energy'].append(float(i[0]))
        output['hours'].append(float(i[1]))
    return output

def pull_daily_lab(lab_name):
    '''pull day data from today table'''
    try:
        mydb = mysql.connector.connect(
        host="energymonitor.princeton.edu",
        user="labenerg_wolson",
        password="lab_energy_monitoring_cos333",
        database ="labenerg_EMDatabase")
    except Exception as ex:
        print("Server error.", ex)
    cursor = mydb.cursor(buffered=True)
    stmt_str = "SELECT total_consumption from today_labinfo "
    stmt_str += "WHERE lab_id = %s;"
    input = [lab_name]
    cursor.execute(stmt_str, input)
    return float((cursor.fetchall()[0][0]))

def pull_daily_fh(lab_name):
    '''pull day data from today table'''
    try:
        mydb = mysql.connector.connect(
        host="energymonitor.princeton.edu",
        user="labenerg_wolson",
        password="lab_energy_monitoring_cos333",
        database ="labenerg_EMDatabase")
    except Exception as ex:
        print("Server error.", ex)
    cursor = mydb.cursor(buffered=True)
    if lab_name == 'rabinowitz_icahn_201':
        fh_cons = {'fh5c': [], 'fh5d': [], 'fh6c': [], 'fh6d':[]}
    elif lab_name == 'rabinowitz_icahn_202':
        fh_cons = {'fh7c': [], 'fh7d': [], 'fh8c': [], 'fh8d':[]}
    stmt_str = "SELECT energy_consumption, hours_open FROM today_fhinfo "
    stmt_str += "WHERE lab_id = %s;"
    input = [lab_name]
    cursor.execute(stmt_str, input)
    output = cursor.fetchall()
    i = 0
    fh_avg_hours = {'fh5c': 12.23, 'fh5d': 14.01, 'fh6c': 8.34, 'fh6d': 10.01, 
    'fh7c': 11.92, 'fh7d': 15.03, 'fh8c': 12.32, 'fh8d': 9.01, }
    for fh in fh_cons.keys():
        fh_cons[fh].append(float(output[i][0]))
        fh_cons[fh].append(float(output[i][1]))
        fh_cons[fh].append(float(fh_avg_hours[fh]))
        i+=1
    return fh_cons

def main():
    print(pull_daily_fh('rabinowitz_icahn_201'))
    # print(pull_daily_lab('rabinowitz_icahn_202'))
    # print(pull_lab_data('daily', 'rabinowitz_icahn_201'))
    # print(pull_lab_data('weekly', 'rabinowitz_icahn_201'))
    # print(pull_lab_data('monthly', 'rabinowitz_icahn_201'))
    # print(pull_lab_data('yearly', 'rabinowitz_icahn_201'))
    # print(pull_lab_data('daily', 'rabinowitz_icahn_201'))
    # print(pull_fh_data('weekly', 'rabinowitz_icahn_201', 'fh5c'))
    # print(pull_fh_data('monthly', 'rabinowitz_icahn_202', 'fh7c'))
    # print(pull_fh_data('yearly', 'rabinowitz_icahn_201', 'fh6c'))
#---------------------------------------------------------
if __name__ == '__main__':
    main()
