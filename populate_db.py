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

def generate_data(num_datapoints):
    data = {}
    output = []
    data = {'rabinowitz_icahn_201': {'fh5c':[], 'fh5d':[], 'fh6c':[], 'fh6d':[]}, 
    'rabinowitz_icahn_202': {'fh7c':[], 'fh8c':[], 'fh7d':[], 'fh8d':[]}}
    for lab in data.keys():
        fumehoods = data[lab]
        for fumehood in fumehoods.keys():
            for i in range(num_datapoints):
                fumehoods[fumehood].append(random_fh_value(5))
    return data

def pop_db(cursor):
    input = []
    data = generate_data(5)
    for lab in data.keys():
        for fumehood in data[lab].keys():
            values = str(data[lab][fumehood])
            input = [fumehood, values, lab]
            stmt_str = "INSERT INTO curr_fhinfo( "
            stmt_str += "fh_id, energy_consumption, lab_id)"
            stmt_str += "VALUES(%s, %s, %s)"
            cursor.execute(stmt_str,input)

def main():
    # Connect to database created with direct server connection
    mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="wolson@Dev",
    database ="energydb")
    cursor = mydb.cursor(buffered=True)
    pop_db(cursor)
    mydb.commit()
    print('success')
#---------------------------------------------------------
if __name__ == '__main__':
    main()
