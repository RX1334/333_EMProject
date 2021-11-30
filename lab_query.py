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
            fh_cons[point] = (((get.json()['Properties'])[0])['Value'])['Value']
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

def time_dates(days=None, weeks=None, months=None, years=None):
    '''return list of list of dates (1week,4weeks,6months,12months) for calculation labels'''
    current_date = date.today()
    dates = []
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
                sixmonths.append(str(curr_month) + '/' +str(int(current_year)-1))
            else:
                sixmonths.append(str(curr_month) + '/' +current_year)
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
                year.append(str(curr_month) + '/' +str(int(current_year)-1))
            else:
                year.append(str(curr_month) + '/' +current_year)
        return year
    week = week_dates()
    month = month_dates()
    sixmonths = six_month_dates()
    year = year_dates()
    return week, month, sixmonths, year


def lab_info():
    root_url = "https://desigocc.princeton.edu/api/api/"
    username = "testuser"
    password = "testuser"
    user_info ="grant_type=password&username=" +  username + "&password=" + password
    r = requests.post(root_url + "token", data=user_info, verify=False)
    # retrieve access token from POST
    token = r.json()['access_token']
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
    labid = 'rabinowitz-icahn-201'

    dict = {'labid': str(labid),
        'rabinowitz_icahn_201-number': fh_opens,
        'rabinowitz_icahn_201-current-kw': str(round(lab_energy, 2)) + ' kW',
        'rabinowitz_icahn_201-today-kwh': str(round(lab_energy*12.379, 2)) + ' kWh',
        'rabinowitz_icahn_201-temperature': str(round(temp)) + ' °F',
        'rabinowitz_icahn_201-fumehood-energy-ratio': '68% Fumehood 32% Other',
        'rabinowitz_icahn_201-occ' : occ,
        'rabinowitz_icahn_201-ave-nrg': str(lab_energy*1.10002) + ' kWh',
        'rabinowitz_icahn_201-nrg-trend': 'NEEDTODO',
        'rabinowitz_icahn_201-chart-data': {
            'dates':  {'labels': [week[0],week[1],week[2],week[3],week[4],week[5], week[6]],
            'time': [450.139, 423.239, 390.291, 320.120, 490.390, 419.329, 213.221]},
            'weeks':  {'labels': [month[0], month[1], month[2], month[3]], 'time': [400.272, 402.002, 381.078, 392.219]},
            'sixMonths': {'labels': [sixmonths[0], sixmonths[1], sixmonths[2], sixmonths[3], sixmonths[4], sixmonths[5]], 'time': [383.382, 392.229, 402.225, 410.202, 402.225, 410.202]},
            'years':  {'labels': [year[0],year[1],year[2], year[3],year[4], year[5], year[6], year[7], year[8], year[9], year[10], year[11]], 'time': [402.208, 303.443, 412.239, 380.393, 390.202, 399.250,
             402.240, 379.992, 389.225, 394.293, 428.393, 402.922]}
        },
        'fumehoods':[
        {'id':'FH5C',
         'kw': str(round(fh_cons['fh5c'], 2)) + ' kWh',
         'kwh': 3,
         'today': 4, 
         'avg-day': 5,
        '-chart-data': {
            'dates':  {'labels': [week[0],week[1],week[2],week[3],week[4],week[5], week[6]],
            'time': [450.139, 423.239, 390.291, 320.120, 490.390, 419.329, 213.221]},
            'weeks':  {'labels': [month[0], month[1], month[2], month[3]], 'time': [400.272, 402.002, 381.078, 392.219]},
            'sixMonths': {'labels': [sixmonths[0], sixmonths[1], sixmonths[2], sixmonths[3], sixmonths[4], sixmonths[5]], 'time': [383.382, 392.229, 402.225, 410.202, 402.225, 410.202]},
            'years':  {'labels': [year[0],year[1],year[2], year[3],year[4], year[5], year[6], year[7], year[8], year[9], year[10], year[11]], 'time': [402.208, 303.443, 412.239, 380.393, 390.202, 399.250,
             402.240, 379.992, 389.225, 394.293, 428.393, 402.922]}
        }, }
        ,
        {'id': 'FH6C',
         'kw': str(round(fh_cons['fh6c'], 2)) + ' kWh', 'kwh': 3,
         'today': 4, 
         'avg-day': 5,
         '-chart-data': {
            'dates':  {'labels': [week[0],week[1],week[2],week[3],week[4],week[5], week[6]],
            'time': [450.139, 423.239, 390.291, 320.120, 490.390, 419.329, 213.221]},
            'weeks':  {'labels': [month[0], month[1], month[2], month[3]], 'time': [400.272, 402.002, 381.078, 392.219]},
            'sixMonths': {'labels': [sixmonths[0], sixmonths[1], sixmonths[2], sixmonths[3], sixmonths[4], sixmonths[5]], 'time': [383.382, 392.229, 402.225, 410.202, 402.225, 410.202]},
            'years':  {'labels': [year[0],year[1],year[2], year[3],year[4], year[5], year[6], year[7], year[8], year[9], year[10], year[11]], 'time': [402.208, 303.443, 412.239, 380.393, 390.202, 399.250,
             402.240, 379.992, 389.225, 394.293, 428.393, 402.922]}
        }, },
        {'id': 'FH5D',
         'kw': str(round(fh_cons['fh5d'], 2)) + ' kWh',
         'kwh': 3, 
         'today': 4,
         'avg-day': 5,
        '-chart-data': {
            'dates':  {'labels': [week[0],week[1],week[2],week[3],week[4],week[5], week[6]],
            'time': [450.139, 423.239, 390.291, 320.120, 490.390, 419.329, 213.221]},
            'weeks':  {'labels': [month[0], month[1], month[2], month[3]], 'time': [400.272, 402.002, 381.078, 392.219]},
            'sixMonths': {'labels': [sixmonths[0], sixmonths[1], sixmonths[2], sixmonths[3], sixmonths[4], sixmonths[5]], 'time': [383.382, 392.229, 402.225, 410.202, 402.225, 410.202]},
            'years':  {'labels': [year[0],year[1],year[2], year[3],year[4], year[5], year[6], year[7], year[8], year[9], year[10], year[11]], 'time': [402.208, 303.443, 412.239, 380.393, 390.202, 399.250,
             402.240, 379.992, 389.225, 394.293, 428.393, 402.922]}
        }, },
        {'id': 'FH6D',
         'kw': str(round(fh_cons['fh6d'], 2)) + ' kWh',
         'kwh': 3,
         'today': 4,
         'avg-day': 5,
        '-chart-data': {
            'dates':  {'labels': [week[0],week[1],week[2],week[3],week[4],week[5], week[6]],
            'time': [450.139, 423.239, 390.291, 320.120, 490.390, 419.329, 213.221]},
            'weeks':  {'labels': [month[0], month[1], month[2], month[3]], 'time': [400.272, 402.002, 381.078, 392.219]},
            'sixMonths': {'labels': [sixmonths[0], sixmonths[1], sixmonths[2], sixmonths[3], sixmonths[4], sixmonths[5]], 'time': [383.382, 392.229, 402.225, 410.202, 402.225, 410.202]},
            'years':  {'labels': [year[0],year[1],year[2], year[3],year[4], year[5], year[6], year[7], year[8], year[9], year[10], year[11]], 'time': [402.208, 303.443, 412.239, 380.393, 390.202, 399.250,
             402.240, 379.992, 389.225, 394.293, 428.393, 402.922]}
        }, }]
    }
    return dict

if __name__ == '__main__':
    lab_info()
