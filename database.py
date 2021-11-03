#!/usr/bin/env python
#-----------------------------------------------------------------------
# Authors: Morgan Teman and Will Olson
#-----------------------------------------------------------------------
from contextlib import closing
from psycopg2 import connect
import psycopg2
from sys import argv, stderr
import sys

# reference to reg.sqlite (read write)
def get_fumehood_output():
        # Connect to an existing database
    connection = psycopg2.connect(user="postgres",
                                  host="127.0.0.1",
                                  port="5432",
                                  database="demolab")

    # Create a cursor to perform database operations
    cursor = connection.cursor()
    # Print PostgreSQL details
    # print("PostgreSQL server information")
    # print(connection.get_dsn_parameters(), "\n")
    outzero = []
    outone = []
    outtwo = []
    outthree = []
    # # Executing a SQL query
    cursor.execute("SELECT * FROM fumehoodzero;")
    outputzero = cursor.fetchall()
    for row in outputzero:
        outzero.append(row[4])
    cursor.execute("SELECT * FROM fumehoodone;")
    outputone = cursor.fetchall()
    for row in outputone:
        outone.append(row[4])
    cursor.execute("SELECT * FROM fumehoodtwo;")
    outputtwo = cursor.fetchall()
    for row in outputtwo:
        outtwo.append(row[4])
    cursor.execute("SELECT * FROM fumehoodthree;")
    outputthree = cursor.fetchall()
    for row in outputthree:
        outthree.append(row[4])
    output = [outzero, outone, outtwo, outthree]
    return output
#------------------------------------------------------------------------------------
if __name__ == '__main__':
    get_fumehood_output()
