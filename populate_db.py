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

def random_fh_value(interval):
    low = ((110/8)/60)/(60/interval)
    high = low + .1
    return round(random.uniform(low, high), 2)

def is_fh_open():
    value = round(random.uniform(0,1), 3)
    return value < .9 #90% probability of 1

def generate_data():
    data = {}
    data = {
    'rabinowitz_icahn_201': {'fumehoods': {'fh5c':[], 'fh5d':[], 'fh6c':[], 'fh6d':[]}}, 
    'rabinowitz_icahn_202': {'fumehoods': {'fh7c':[], 'fh8c':[], 'fh7d':[], 'fh8d':[]}}}
    for lab in data.keys():
        fumehoods = data[lab]['fumehoods']
        for fumehood in fumehoods.keys():
            open = is_fh_open()
            if open:
                fumehoods[fumehood].append(open)
                fumehoods[fumehood].append(random_fh_value(5))
            else:
                fumehoods[fumehood].append(open)
                fumehoods[fumehood].append(0)
    return data

def pop_fh_db(cursor, time):
    data = generate_data()
    for lab in data.keys():
        values = data[lab]['fumehoods']
        for fumehood in values.keys():
            cons = []
            hours = []
            vals = data[lab]['fumehoods'][fumehood]
            for _ in range(time):
                cons.append(round(random.uniform(370, 455), 2))
                hours.append(round(random.uniform(90, 120), 2))
            if time == 7:
                for i in range(time):
                    input = [fumehood+'_'+str(i),fumehood,i,lab, cons[i],hours[i]]
                    stmt_str = "INSERT INTO week_fhinfo( "
                    stmt_str += "id,fh_id,lab_id,day,energy_consumption,hours_open)"
                    stmt_str += "VALUES(%s,%s,%s,%s,%s,%s)"
                    cursor.execute(stmt_str,input)
            if time == 4:
                for i in range(time):
                    input = [fumehood+'_'+str(i),fumehood,i,lab, cons[i],hours[i]]
                    stmt_str = "INSERT INTO month_fhinfo( "
                    stmt_str += "id,fh_id,lab_id,week,energy_consumption,hours_open)"
                    stmt_str += "VALUES(%s,%s,%s,%s,%s,%s)"
                    cursor.execute(stmt_str,input)
            if time == 12:
                for i in range(time):
                    input = [fumehood+'_'+str(i),fumehood,i,lab, cons[i],hours[i]]
                    stmt_str = "INSERT INTO year_fhinfo( "
                    stmt_str += "id,fh_id,lab_id,month,energy_consumption,hours_open)"
                    stmt_str += "VALUES(%s,%s,%s,%s,%s,%s)"
                    cursor.execute(stmt_str,input)

def pop_lab_db(cursor, time):
    labs = ['rabinowitz_icahn_201', 'rabinowitz_icahn_202']
    for lab in labs:
        cons = []
        opens = []
        totals = []
        for _ in range(time):
            cons.append(round(random.uniform(370*4, 455*4), 2))
            opens.append(round(random.uniform(2,4), 2))
            totals.append(round(random.uniform(650, 750), 2))
        if time == 7:
            for i in range(time):
                input = [lab+'_'+str(i),lab,i, cons[i], opens[i],totals[i]]
                stmt_str = "INSERT INTO week_labinfo( "
                stmt_str += "id,lab_id,day,fh_consumption,fh_opens,avg_consumption)"
                stmt_str += "VALUES(%s,%s,%s,%s,%s,%s)"
                cursor.execute(stmt_str,input)
        if time == 4:
            for i in range(time):
                input = [lab+'_'+str(i),lab,i, cons[i], opens[i],totals[i]]
                stmt_str = "INSERT INTO month_labinfo( "
                stmt_str += "id,lab_id,week,fh_consumption,fh_opens,avg_consumption)"
                stmt_str += "VALUES(%s,%s,%s,%s,%s, %s)"
                cursor.execute(stmt_str,input)
        if time == 12:
            for i in range(time):
                input = [lab+'_'+str(i),lab,i, cons[i], opens[i],totals[i]]
                stmt_str = "INSERT INTO year_labinfo( "
                stmt_str += "id,lab_id,month,fh_consumption,fh_opens,avg_consumption)"
                stmt_str += "VALUES(%s,%s,%s,%s,%s, %s)"
                cursor.execute(stmt_str,input)

def main():
    # Connect to database created with direct server connection
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="wolson@Dev",
    database ="energydb")
    cursor = mydb.cursor(buffered=True)
    pop_fh_db(cursor, 7) # week
    pop_fh_db(cursor, 4) # week
    pop_fh_db(cursor, 12) # year
    pop_lab_db(cursor, 7) # week
    pop_lab_db(cursor, 4) # week
    pop_lab_db(cursor, 12) # year
    mydb.commit()
#---------------------------------------------------------
if __name__ == '__main__':
    main()
