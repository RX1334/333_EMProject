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
    print('lol')
    # # we will only ever post to the day table from here - all other updates will occur in cron/on cpanel
    # '''get the average fumehood consumption for a given date'''
    # conn = pymysql.connect(host='67.205.146.88',
    #                          user='labenergy',
    #                          password='lab_energy_monitoring_cos333',                             
    #                          db='labenerg_energydb',
    #                          charset='utf8mb4',
    #                          cursorclass=pymysql.cursors.DictCursor)
    # try:  
    #     with conn.cursor() as cursor: 
    #         stmt_str = "INSERT INTO day_fhinfo (consumption) values (%s)"
    #         cursor.execute(stmt_str, fh_id)
    # finally:
    #     # Close connection.
    #     conn.close()
def nrg_trend():
    # We want this just be short numerical info (otherwise the display is clunky). 
    # The helper text in the html file handles this fine. Also, %'s don't need to 
    # be escaped
    return('-8.2%')

def put_lab_info():
    print('lol')

def get_lab_info():
    return {'dates':[450.139, 423.239, 390.291, 320.120, 490.390, 419.329, 213.221], 'weeks':[400.272, 402.002, 381.078, 392.219], 'sixMonths':[383.382, 392.229, 402.225, 410.202, 402.225, 410.202], 'years': [402.208, 303.443, 412.239, 380.393, 390.202, 399.250,
             402.240, 379.992, 389.225, 394.293, 428.393, 402.922]}

def week_report(date):
    return {'this_week_energy_consumption': '323.3 kWh',
    'this_week_avg_power_consumption': '421.23 kWh', 
    'this_week_avg_fumehood_usage': '6 hrs', 
    'energy_consumption_kwh_day': [3,3,3,3,3,3,3,], 
    'energy_consumption_dollar_day': [5,5,5,5,5,5,5], 
    'energy_consumption_lb_co2_day': [8,8,8,8,8,8,8]}

def get_fumehood_output(fh_id):
    #return dict of fumehood:dict{time1:list1, time2:list2,time3:list3, time4:list4}
    if fh_id == '5c':
        return {'dates':[450.139, 423.239, 390.291, 320.120, 490.390, 419.329, 213.221], 'weeks':[400.272, 402.002, 381.078, 392.219], 'sixMonths':[383.382, 392.229, 402.225, 410.202, 402.225, 410.202], 'years': [402.208, 303.443, 412.239, 380.393, 390.202, 399.250,
             402.240, 379.992, 389.225, 394.293, 428.393, 402.922]}
    if fh_id == '5d':
        return {'dates':[450.139, 423.239, 390.291, 320.120, 490.390, 419.329, 213.221], 'weeks':[400.272, 402.002, 381.078, 392.219], 'sixMonths':[383.382, 392.229, 402.225, 410.202, 402.225, 410.202], 'years':[402.208, 303.443, 412.239, 380.393, 390.202, 399.250,
             402.240, 379.992, 389.225, 394.293, 428.393, 402.922]}
    if fh_id == '6c':
        return {'dates':[450.139, 423.239, 390.291, 320.120, 490.390, 419.329, 213.221], 'weeks':[400.272, 402.002, 381.078, 392.219], 'sixMonths':[383.382, 392.229, 402.225, 410.202, 402.225, 410.202], 'years': [402.208, 303.443, 412.239, 380.393, 390.202, 399.250,
             402.240, 379.992, 389.225, 394.293, 428.393, 402.922]}
    if fh_id == '6d':
        return {'dates':[450.139, 423.239, 390.291, 320.120, 490.390, 419.329, 213.221], 'weeks':[400.272, 402.002, 381.078, 392.219], 'sixMonths':[383.382, 392.229, 402.225, 410.202, 402.225, 410.202], 'years': [402.208, 303.443, 412.239, 380.393, 390.202, 399.250,
             402.240, 379.992, 389.225, 394.293, 428.393, 402.922]}
    
    # # time range determines which table to query from 
    # if tabletime == 'day':
    #     timerange = 'day_fhinfo'
    # elif tabletime == 'week':
    #     timerange = 'week_fhinfo'
    # elif tabletime == 'month':
    #     timerange = 'month_fhinfo'
    # else:
    #     timerange = 'year_fhinfo'

    # '''get the average fumehood consumption for a given date'''
    # conn = pymysql.connect(host='67.205.146.88',
    #                          user='labenergy',
    #                          password='lab_energy_monitoring_cos333',                             
    #                          db='labenerg_energydb',
    #                          charset='utf8mb4',
    #                          cursorclass=pymysql.cursors.DictCursor)
    # try:  
    #     with conn.cursor() as cursor: 
    #         stmt_str = "SELECT * FROM %s WHERE id=%s AND date=%s"
    #         cursor.execute(stmt_str, timerange, date, fh_id)
    #         if cursor.rowcount == 0: 
    #             return('ERROR: DATA FOR DATE ' +date+ ' NOT FOUND.')
    #         else:
    #             return(cursor.fetchone()) 
    # finally:
    #     # Close connection.
    #     conn.close()

def put_lab_info(date, fh_id):
    print('haha')
    # # we will only ever post to the day table from here - all other updates will occur in cron/on cpanel
    # '''get the average fumehood consumption for a given date'''
    # conn = pymysql.connect(host='67.205.146.88',
    #                          user='labenergy',
    #                          password='lab_energy_monitoring_cos333',                             
    #                          db='labenerg_energydb',
    #                          charset='utf8mb4',
    #                          cursorclass=pymysql.cursors.DictCursor)
    # try:  
    #     with conn.cursor() as cursor: 
    #         stmt_str = "INSERT INTO day_labinfo (consumption) values (%s)"
    #         cursor.execute(stmt_str, fh_id)
    # finally:
    #     # Close connection.
    #     conn.close()

# # def put_fumehood_output(date, cursor, value):
# def get_lab_info(tabletime, date, fh_id):
#     # time range determines which table to query from 
#     if tabletime == 'day':
#         timerange = 'day_labinfo'
#     elif tabletime == 'week':
#         timerange = 'week_labinfo'
#     elif tabletime == 'month':
#         timerange = 'month_labinfo'
#     else:
#         timerange = 'year_labinfo'

#     '''get the average fumehood consumption for a given date'''
#     conn = pymysql.connect(host='67.205.146.88',
#                              user='labenergy',
#                              password='lab_energy_monitoring_cos333',                             
#                              db='labenerg_energydb',
#                              charset='utf8mb4',
#                              cursorclass=pymysql.cursors.DictCursor)
#     try:  
#         with conn.cursor() as cursor: 
#             stmt_str = "SELECT * FROM %s WHERE id=%s AND date=%s"
#             cursor.execute(stmt_str, timerange, date, fh_id)
#             if cursor.rowcount == 0: 
#                 return('ERROR: DATA FOR DATE ' +date+ ' NOT FOUND.')
#             else:
#                 return(cursor.fetchone()) 
#     finally:
#         # Close connection.
#         conn.close()

def main():
    get_fumehood_output(1,2)

    
#---------------------------------------------------------
if __name__ == '__main__':
    main()
