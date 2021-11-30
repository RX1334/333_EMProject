#!/usr/bin/env python
#-----------------------------------------------------------------------
# Authors: abc123
# source ~/.virtualenvs/cos333/bin/activate
#-----------------------------------------------------------------------
import os
import json
import requests
import urllib3
import time
from datetime import date, timedelta
from database import put_fumehood_output, get_fumehood_output, put_lab_info, get_lab_info
from database import nrg_trend, week_report

# disable https warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# unit toggle - return dollars or kwh
money_mode = 0

#constants
CONVERSION_FACTOR = 24.4243395
BUSINESS_DAYS = 261.0
HOURS = 8.0
LAB_SIZE = 9000.0

def set_units(mode):
    '''toggle units for dashboard - either dollar values or energy metrics'''
    if mode == 'money':
        money_mode = 1
    else:
        money_mode = 0


def occupancy(root_url, token):
    '''total number of lab occupants'''
    occ_w = "System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-cscs-apog305.Local_IO.B47_RML210_OS1;"
    occ_e = "System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-csc-apog306.Local_IO.B47_RML210_OS2;"
    occ_req1 = requests.get(root_url + occ_w, headers={'Authorization': 'Bearer ' + token}, verify=False)
    occ_req2 = requests.get(root_url + occ_e, headers={'Authorization': 'Bearer ' + token}, verify=False)
    print(occ_req1)

    # calculate total occupancy
    return(int((((occ_req1.json()['Properties'])[0])['Value'])['Value']) + int((((occ_req2.json()['Properties'])[0])['Value'])['Value']))

def fh_open(root_url, token):
    '''dict containing the four fumehoods and their open/closed status as strings
    note: uses fumehood percent open as a proxy for on/off, with 5% as the threshold'''
    fh_opens = {'fh5c': 0, 'fh5d':0, 'fh6c':0, 'fh6d':0}
    points = ["System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-cscs-apog305.Local_IO.B47_FH5C_FAO;",
    "System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-cscs-apog305.Local_IO.B47_FH6C_FAO;",
    "System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-csc-apog306.Local_IO.B47_FH5D_FAO;",
    "System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-csc-apog306.Local_IO.B47_FH6D_FAO;"]
    output = []
    for point in points:
        output.append(requests.get(root_url + point, headers={'Authorization': 'Bearer ' + token}, verify=False))
    fh_opens['fh5c'] = (((output[0].json()['Properties'])[0])['Value'])['Value']
    fh_opens['fh6c'] = (((output[1].json()['Properties'])[0])['Value'])['Value']
    fh_opens['fh5d'] = (((output[2].json()['Properties'])[0])['Value'])['Value']
    fh_opens['fh6d'] = (((output[3].json()['Properties'])[0])['Value'])['Value']
    # create dict of fh open/closed status
    for fh in fh_opens.keys():
        if float(fh_opens[fh]) > 5.0:
            fh_opens[fh] = "OPEN"
        else:
            fh_opens[fh] = "CLOSED"
    return fh_opens

def lights_open(root_url, token):
    '''returns dict of lights (east/west) and their on/off status'''
    lights_open = {'west': 0, 'east': 0}
    points = ["System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-cscs-apog305.Local_IO.B47_2FWL_LM1;",
    "System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-csc-apog306.Local_IO.B47_2FWL_LM2;"]
    output = []
    for point in points:
        output.append(requests.get(root_url + point, headers={'Authorization': 'Bearer ' + token}, verify=False))
    lights_open['west'] = (((output[0].json()['Properties'])[0])['Value'])['Value']
    lights_open['east'] = (((output[1].json()['Properties'])[0])['Value'])['Value']
    return lights_open

def climate_energy(root_url, token):
    '''returns approximate energy usage of climate control devices'''
    points = ["System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-cscs-apog305.Local_IO.B47_RML2-2_SPT;"]
    x = requests.get(root_url + points[0], headers={'Authorization': 'Bearer ' + token}, verify=False)
    temp = (((x.json()['Properties'])[0])['Value'])['Value']
    return 0.1*float(temp)

def fh_consumption(root_url, token, fh_opens):
    '''input: dict of fumehoods open/closed status
    output: dict of fumehoods and their approximate energy status
    see: https://fumehoodcalculator.lbl.gov/'''
    fh_cons = {'fh5c': [0], 'fh5d': [0], 'fh6c': [0], 'fh6d':[0]}
    for fh in fh_opens.keys():
        if fh_opens[fh] == 'OPEN':
            fh_cons[fh][0] = 1
    fh_cons['fh5c'].append("System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-cscs-apog305.FLN_1.B47_FHET1-5C.EXH_FLOW;")
    fh_cons['fh6c'].append("System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-csc-apog306.FLN_1.B47_FHET1-6C.EXH_FLOW;")
    fh_cons['fh5d'].append("System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-csc-apog306.FLN_1.B47_FHET1-5D.EXH_FLOW;")
    fh_cons['fh6d'].append("System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-csc-apog306.FLN_1.B47_FHET1-6D.EXH_FLOW;")
    # print(fh_cons)
    output = []
    for point in fh_cons.keys():
        if fh_cons[point][0] == 1:
            get = requests.get(root_url + fh_cons[point][1], headers={'Authorization': 'Bearer ' + token}, verify=False)
            try:
                fh_cons[point] = (((get.json()['Properties'])[0])['Value'])['Value']
            except:
                fh_cons[point] = 0.0
        else:
            fh_cons[point] = 0.0
    # print(fh_cons)
    return fh_cons

def energy_calc(fh_cons):
    '''input: a dictionary of fumehoods and their current exh flow in cfm
       output: a dictionary of fumehoods and their current consumption in kwh'''
    for fh in fh_cons.keys():
        if fh_cons[fh] == 'OFF':
            fh_cons[fh] == 0.0
        else:
            fh_cons[fh] = float(fh_cons[fh])*CONVERSION_FACTOR/BUSINESS_DAYS/HOURS
    return fh_cons

def lab_energy_calc(fh_cons, climate):
    out = 0.0
    for fh in fh_cons.keys():
        out += fh_cons[fh]
    out += climate
    return out

def lab_money_calc(fh_cons, climate):
    out = 0.0
    for fh in fh_cons.keys():
        out += fh_cons[fh]
    out += climate
    return out*2.25

def time_dates(date_input=None):
    '''return list of list of dates (1week,4weeks,6months,12months) for calculation labels'''
    if date_input is not None:
        current_date = date_input
    else:
        current_date = date.today()
    dates = []
    def month_tostring(month):
        monthnames = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEP', 'OCT', 'NOV', 'DEC']
        return monthnames[month-1]
    # 1 week by day
    def week_dates():
        week = []
        for i in range(7):
            day = str((current_date - timedelta(days=(6-i))).strftime("%m/%d"))
            week.append(day)
        dates.append(week)
        return week
    # 1 month by week
    def month_dates():
        month = []
        for i in range(4):
            # reverse order of list
            i = 3-i
            week_start = current_date - timedelta(weeks=i)
            week_end = (current_date + timedelta(weeks = 1)) - timedelta(weeks=i)
            str = week_start.strftime("%m/%d")+ "-" + week_end.strftime("%m/%d")
            month.append(str)
        return month
    # six months by month
    def six_month_dates():
        current_month = date.today().strftime("%m")
        current_year = str(date.today().strftime("%y"))
        sixmonths = []
        for i in range(6):
            curr_month = int(current_month)-i
            if curr_month < 1:
                curr_month = 12-curr_month
                sixmonths.append(month_tostring(curr_month) + " " + str(int(current_year)-1))
            else:
                sixmonths.append(month_tostring(curr_month) + " " + current_year)
        return sixmonths
    # 1 year by month
    def year_dates():
        current_month = date.today().strftime("%m")
        current_year = str(date.today().strftime("%y"))
        year = []
        for i in range(12):
            curr_month = int(current_month)-i
            if curr_month < 1:
                curr_month = 12-curr_month
                year.append(month_tostring(curr_month) + ' ' +str(int(current_year)-1))
            else:
                year.append(month_tostring(curr_month) + ' ' +current_year)
        return year
    week = week_dates()
    month = month_dates()
    sixmonths = six_month_dates()
    year = year_dates()
    return week, month, sixmonths, year

def graph_info():
    return(0)

def weekly_report(week_date):
    # need to add logic for consistent start date (e.g. every sunday)
    data = week_report()
    cal = time_dates(week_date)
    dict = {'date': week_date,
    'week': cal[2],
    'this_week_energy_consumption': data['this_week_energy_consumption'],
    'this_week_avg_power_consumption': data['this_week_avg_power_consumption'],
    'this_week_avg_fumehood_usage': data['this_week_avg_power_consumption'],
    'energy_consumption_kwh_day': data['this_week_avg_power_consumption'],
    'energy_consumption_dollar_day': data['this_week_avg_power_consumption'],
    'energy_consumption_lb_co2_day': data['this_week_avg_power_consumption']}
    return dict

def lab_info():
    root_url = "https://desigocc.princeton.edu/api/api/"
    username = "testuser"
    password = "testuser"
    user_info ="grant_type=password&username=" +  username + "&password=" + password
    r = requests.post(root_url + "token", data=user_info, verify=False)
    # retrieve access token from POST
    token = r.json()['access_token']
    print(token)
    # lab occupancy (1 west, 2 east)
    root_url += "propertyvalues/"
    # calculate total occupancy
    occ = occupancy(root_url, token)
    fh_opens = fh_open(root_url, token)
    light_opens = lights_open(root_url, token)
    fh_cons = fh_consumption(root_url, token, fh_opens)
    # calculate energy usage from airflow, modify existing dict
    energy_calc(fh_cons)
    climate = climate_energy(root_url, token)
    if money_mode:
        lab_energy = lab_energy_calc(fh_cons, climate)
    else:
        lab_energy = lab_money_calc(fh_cons, climate)
    temp = climate*10
    times = time_dates()
    week = times[0]
    month = times[1]
    sixmonths = times[2]
    year = times[3]
    info_5c = get_fumehood_output('5c')
    info_5d = get_fumehood_output('5d')
    info_6c = get_fumehood_output('6c')
    info_6d = get_fumehood_output('6d')
    info_lab = get_lab_info()
    energy_comp = nrg_trend()

    labid = 'rabinowitz_icahn_201'

    dict = {'labid': str(labid),
        'rabinowitz_icahn_201-number': fh_opens,
        'rabinowitz_icahn_201-current-kw': str(round(lab_energy, 2)) + ' kW',
        'rabinowitz_icahn_201-today-kwh': str(round(lab_energy*12.379, 2)) + ' kWh',
        'rabinowitz_icahn_201-temperature': str(round(temp)) + ' °F',
        'rabinowitz_icahn_201-fumehood-energy-ratio': '68%% Fumehood 32%% Other',
        'rabinowitz_icahn_201-occ' : occ,
        'rabinowitz_icahn_201-ave-nrg': str(lab_energy*1.10002) + ' kWh',
        'rabinowitz_icahn_201-nrg-trend': energy_comp,
        'rabinowitz_icahn_201-chart-data': {
            'dates':  {'labels': week, 'time': info_lab['dates']},
            'weeks':  {'labels': month, 'time':info_lab['weeks']},
            'sixMonths': {'labels': sixmonths, 'time': info_lab['sixMonths']},
            'years':  {'labels': year, 'time': info_lab['years']}
        },
        'fumehoods':[
        {'id':'FH5C',
         'kw': str(round(fh_cons['fh5c'], 2)) + ' kWh',
         'kwh': 3,
         'today': 4,
         'avg-day': 5,
        '-chart-data': {
            'dates':  {'labels': week, 'time': info_5c['dates']},
            'weeks':  {'labels': month, 'time': info_5c['weeks']},
            'sixMonths': {'labels': sixmonths, 'time': info_5c['sixMonths']},
            'years':  {'labels': year, 'time': info_5c['years']}
        }, }
        ,
        {'id': 'FH6C',
         'kw': str(round(fh_cons['fh6c'], 2)) + ' kWh', 'kwh': 3,
         'today': 4,
         'avg-day': 5,
         '-chart-data': {
            'dates':  {'labels': week, 'time': info_6c['dates']},
            'weeks':  {'labels': month, 'time': info_6c['weeks']},
            'sixMonths': {'labels': sixmonths, 'time': info_6c['sixMonths']},
            'years':  {'labels': year, 'time': info_6c['years']}
        }, },
        {'id': 'FH5D',
         'kw': str(round(fh_cons['fh5d'], 2)) + ' kWh',
         'kwh': 3,
         'today': 4,
         'avg-day': 5,
        '-chart-data': {
            'dates':  {'labels': week, 'time': info_5d['dates']},
            'weeks':  {'labels': month, 'time': info_5d['weeks']},
            'sixMonths': {'labels': sixmonths, 'time': info_5d['sixMonths']},
            'years':  {'labels': year, 'time': info_5d['years']}
        }, },
        {'id': 'FH6D',
         'kw': str(round(fh_cons['fh6d'], 2)) + ' kWh',
         'kwh': 3,
         'today': 4,
         'avg-day': 5,
        '-chart-data': {
            'dates':  {'labels': week, 'time': info_6d['dates']},
            'weeks':  {'labels': month, 'time': info_6d['weeks']},
            'sixMonths': {'labels': sixmonths, 'time': info_6d['sixMonths']},
            'years':  {'labels': year, 'time': info_6d['years']}
        }, }]
    }
    # put_fumehood_output()
    # put_lab_info()
    print(dict)
    return dict

if __name__ == '__main__':
    lab_info()
