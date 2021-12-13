#!/usr/bin/env python
#-----------------------------------------------------------------------
# Authors: abc123
# source ~/.virtualenvs/cos333/bin/activate
#-----------------------------------------------------------------------
import json, requests, os, time, random
import string as strng
from datetime import date, timedelta, datetime
from push_db import put_fh_db, put_lab_db
from pull_db import pull_fh_data, pull_lab_data, week_report

# disable https warning
# urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

#constants
CONVERSION_FACTOR = 24.4243395
BUSINESS_DAYS = 261.0
HOURS = 8.0
LAB_SIZE = 9000.0

def occupancy(root_url, token, lab_id):
    '''total number of lab occupants'''
    # occ_w = "System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-cscs-apog305.Local_IO.B47_RML210_OS1;"
    # occ_e = "System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-csc-apog306.Local_IO.B47_RML210_OS2;"
    # occ_req1 = requests.get(root_url + occ_w, headers={'Authorization': 'Bearer ' + token}, verify=False)
    # occ_req2 = requests.get(root_url + occ_e, headers={'Authorization': 'Bearer ' + token}, verify=False)
    # # calculate total occupancy
    # return(int((((occ_req1.json()['Properties'])[0])['Value'])['Value']) + int((((occ_req2.json()['Properties'])[0])['Value'])['Value']))
    # returns 0 if past 6pm
    if datetime.now().time().hour > 17:
        return 0
    else:
        return 3

def fh_open(root_url, token, lab_id):
    # '''dict containing the four fumehoods and their open/closed status as strings
    # note: uses fumehood percent open as a proxy for on/off, with 5% as the threshold'''
    fh_opens = {'fh5c': 0, 'fh5d':0, 'fh6c':0, 'fh6d':0}
    # points = ["System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-cscs-apog305.Local_IO.B47_FH5C_FAO;",
    # "System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-cscs-apog305.Local_IO.B47_FH6C_FAO;",
    # "System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-csc-apog306.Local_IO.B47_FH5D_FAO;",
    # "System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-csc-apog306.Local_IO.B47_FH6D_FAO;"]
    # output = []
    # for point in points:
    #     output.append(requests.get(root_url + point, headers={'Authorization': 'Bearer ' + token}, verify=False))
    # fh_opens['fh5c'] = (((output[0].json()['Properties'])[0])['Value'])['Value']
    # fh_opens['fh6c'] = (((output[1].json()['Properties'])[0])['Value'])['Value']
    # fh_opens['fh5d'] = (((output[2].json()['Properties'])[0])['Value'])['Value']
    # fh_opens['fh6d'] = (((output[3].json()['Properties'])[0])['Value'])['Value']
    # # create dict of fh open/closed status
    # for fh in fh_opens.keys():
    #     if float(fh_opens[fh]) > 5.0:
    #         fh_opens[fh] = "OPEN"
    #     else:
    #         fh_opens[fh] = "CLOSED"
    # return fh_opens
    if lab_id == 'rabinowitz_icahn_201':
        return {'fh5c': 'OPEN', 'fh5d':'OPEN', 'fh6c':'CLOSED', 'fh6d':'OPEN'}
    else:
        return {'fh7c': 'OPEN', 'fh7d':'OPEN', 'fh8c':'OPEN', 'fh8d':'CLOSED'}


def lights_open(root_url, token, lab_id):
    '''returns dict of lights (east/west) and their on/off status'''
    # lights_open = {'west': 0, 'east': 0}
    # points = ["System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-cscs-apog305.Local_IO.B47_2FWL_LM1;",
    # "System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-csc-apog306.Local_IO.B47_2FWL_LM2;"]
    # output = []
    # for point in points:
    #     output.append(requests.get(root_url + point, headers={'Authorization': 'Bearer ' + token}, verify=False))
    # lights_open['west'] = (((output[0].json()['Properties'])[0])['Value'])['Value']
    # lights_open['east'] = (((output[1].json()['Properties'])[0])['Value'])['Value']
    # return lights_open
    if datetime.now().time().hour > 17:
        return {'west': 1, 'east': 0}
    else:
        return {'west': 1, 'east': 1}

def climate_energy(root_url, token, lab_id):
    # '''returns approximate energy usage of climate control devices'''
    # points = ["System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-cscs-apog305.Local_IO.B47_RML2-2_SPT;"]
    # x = requests.get(root_url + points[0], headers={'Authorization': 'Bearer ' + token}, verify=False)
    # temp = (((x.json()['Properties'])[0])['Value'])['Value']
    # return 0.1*float(temp)
    return round(random.uniform(.003,.008), 3)


def fh_consumption(root_url, token, fh_opens, lab_id):
    '''input: dict of fumehoods open/closed status
    output: dict of fumehoods and their approximate energy status
    # see: https://fumehoodcalculator.lbl.gov/'''
    if lab_id == 'rabinowitz_icahn_201':
        fh_cons = {'fh5c': [0], 'fh5d': [0], 'fh6c': [0], 'fh6d':[0]}
    else:
        fh_cons = {'fh7c': [0], 'fh7d': [0], 'fh8c': [0], 'fh8d':[0]}
    for fh in fh_opens.keys():
        if fh_opens[fh] == 'OPEN':
            fh_cons[fh][0] = 1
    # fh_cons['fh5c'].append("System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-cscs-apog305.FLN_1.B47_FHET1-5C.EXH_FLOW;")
    # fh_cons['fh6c'].append("System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-csc-apog306.FLN_1.B47_FHET1-6C.EXH_FLOW;")
    # fh_cons['fh5d'].append("System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-csc-apog306.FLN_1.B47_FHET1-5D.EXH_FLOW;")
    # fh_cons['fh6d'].append("System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-csc-apog306.FLN_1.B47_FHET1-6D.EXH_FLOW;")
    # output = []
    # for point in fh_cons.keys():
    #     if fh_cons[point][0] == 1:
    #         get = requests.get(root_url + fh_cons[point][1], headers={'Authorization': 'Bearer ' + token}, verify=False)
    #         fh_cons[point] = (((get.json()['Properties'])[0])['Value'])['Value']
    #     else:
    #         fh_cons[point] = 0.0
    i = 0
    for fh in fh_opens.keys():
        if fh_opens[fh] == 'OPEN':
            fh_cons[fh].append(round(random.uniform(10,12), 3))
        else:
            fh_cons[fh].append(0)
        # Fake random data for today energy, hrs today, ave hrs
        fh_cons[fh].append(round((3 + i) *random.uniform(0.8,1.2), 2))
        fh_cons[fh].append(round((4 + i) *random.uniform(0.8,1.2), 2))
        fh_cons[fh].append(round((5 + i) *random.uniform(0.8,1.2), 2))
        i += 1


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

def lab_energy_calc(fh_cons, climate, lab_id):
    out = 0.0
    for fh in fh_cons.keys():
        out += fh_cons[fh][1]
    out += climate
    return out

def report_archive_dates(lab_id):
    if (lab_id == 'rabinowitz_icahn_201'):
        lab_id_number = 12
    else:
        lab_id_number = 8
    current_date = date.today()
    weeks = []
    for i in range(1,lab_id_number):
        week = current_date - timedelta(weeks=i)
        str = week.strftime("%m")+ "." + week.strftime("%d") + "." + week.strftime("%y")
        weeks.append(str)
    return weeks

def time_dates(date_input=None):
    '''return list of list of dates (1week,4weeks,6months,12months) for calculation labels'''
    if date_input is not None:
        month = date_input.split('.')[0]
        day = date_input.split('.')[1]
        current_date = datetime(2021, int(month), int(day))
        # current_date = dat.strftime("%m/%d")
    else:
        current_date = date.today()
    dates = []
    def month_tostring(month):
        monthnames = ['JAN', 'FEB', 'MAR', 'APR', 'MAY', 'JUN', 'JUL', 'AUG', 'SEPT', 'OCT', 'NOV', 'DEC']
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
    # 1 year by month
    def months_dates():
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
    def year_dates():
        current_year = str(date.today().strftime("%y"))
        years = []
        for i in range(5):
             years.append(int(str(20)+current_year)-i)
        return years
    week = week_dates()
    month = month_dates()
    months = months_dates()
    years = year_dates()
    return week, month, months, years

def weekly_report(lab_name, week_date):
    # need to add logic for consistent start date (e.g. every sunday)
    data = week_report(lab_name, week_date)
    energy, power, usage, energy_cons, dollars, co2 = [[],[],[],[],[],[]]
    for _ in range(7):
        energy.append(round(data[0]*random.uniform(0.5,1), 2))
        power.append(round(data[0]*random.uniform(0.5,1), 2))
        usage.append(round(random.uniform(8,12), 2))
        energy_cons.append(round(data[0]*random.uniform(0.5,1), 2))
        # dollars.append(round(random.uniform(8,12), 2))
        dollars.append(round(energy_cons[-1] * 2.25, 2))
        # co2.append(round(random.uniform(10,12), 2))
        co2.append(round(energy_cons[-1] * 0.85, 2))
    mo = week_date.split('.')[0]
    day = week_date.split('.')[1]
    forward_date = datetime(2021, int(mo), int(day))
    forward_date = (forward_date + timedelta(weeks=1) - timedelta(days=1)).strftime("%m.%d")
    cal = time_dates(forward_date)[0]
    dict = {'date': week_date,
    'week': cal,
    'this_week_energy_consumption': str(round(sum(energy), 2)) + ' kWh',
    'this_week_avg_power_consumption': str(round(sum(power)/len(power),2)) + ' kW',
    'this_week_avg_fumehood_usage': str(round(sum(usage)/len(usage), 2)) + ' Hrs',
    'energy_consumption_kwh_day': energy_cons,
    'energy_consumption_dollars_day': dollars,
    'energy_consumption_lb_co2_day': co2}
    return dict

def get_fumehoods(lab_name):
    if lab_name == 'rabinowitz_icahn_201':
        return ['fh5c', 'fh5d', 'fh6c', 'fh6d']
    if lab_name == 'rabinowitz_icahn_202':
        return ['fh7c', 'fh7d', 'fh8c', 'fh8d']

def graph_info(lab_name):
    days, weeks, months, years = time_dates()
    fumehoods = get_fumehoods(lab_name)
    daily_lab = pull_lab_data('daily', lab_name)
    weekly_lab = pull_lab_data('weekly', lab_name)
    monthly_lab = pull_lab_data('monthly', lab_name)
    yearly_lab = pull_lab_data('yearly', lab_name)
    dict = {lab_name+ '-chart-data': {
        'daily':  {'labels': days, 'time': daily_lab['total']},
        'weekly':  {'labels': weeks, 'time':weekly_lab['total']},
        'monthly': {'labels': months, 'time': monthly_lab['total']},
        'yearly':  {'labels': years, 'time': yearly_lab['total']}},
        'fumehoods':[]}
    for fumehood in fumehoods:
        daily_fh = pull_fh_data('daily', lab_name,fumehood)
        weekly_fh = pull_fh_data('weekly', lab_name,fumehood)
        monthly_fh = pull_fh_data('monthly', lab_name,fumehood)
        yearly_fh = pull_fh_data('yearly', lab_name,fumehood)
        dict['fumehoods'].append({'id': fumehood,
        '-chart-data':{'daily':  {'labels': days, 'time': daily_fh['energy']},
                    'weekly':  {'labels': weeks, 'time': weekly_fh['energy']},
                    'monthly': {'labels': months, 'time': monthly_fh['energy']},
                    'yearly':  {'labels': years, 'time': yearly_fh['energy']}}})
    return dict

def lab_info(lab_name):
    # root_url = "https://desigocc.princeton.edu/api/api/"
    # username = "testuser"
    # password = "testuser"
    # user_info ="grant_type=password&username=" +  username + "&password=" + password
    # r = requests.post(root_url + "token", data=user_info, verify=False)
    # # retrieve access token from POST
    # token = r.json()['access_token']
    # # lab occupancy (1 west, 2 east)
    # root_url += "propertyvalues/"
    root_url = None
    token = None
    # calculate total occupancy
    occ = occupancy(root_url, token, lab_name)
    fh_opens = fh_open(root_url, token, lab_name)
    light_opens = lights_open(root_url, token, lab_name)
    fh_cons = fh_consumption(root_url, token, fh_opens, lab_name)
    climate = climate_energy(root_url, token, lab_name)
    lab_compares = {'rabinowitz_icahn_201': '8.9%',
    'rabinowitz_icahn_202': '6.4%'}
    lab_ratios = {'rabinowitz_icahn_201': '68% Fumehood 32% Other',
    'rabinowitz_icahn_202': '74% Fumehood 26% Other'}
    total_fh_push = 0
    for fh in fh_cons.keys():
        total_fh_push += fh_cons[fh][1]
    lab_energy = total_fh_push + climate
    put_lab_db(lab_name, total_fh_push, climate,lab_energy)
    fh_names = get_fumehoods(lab_name)
    for fh in fh_names:
        if fh_opens[fh] == 'OPEN':
            put_fh_db(fh, lab_name, fh_cons[fh][1], 1)
        else:
            put_fh_db(fh, lab_name, fh_cons[fh][1], 0)
    print(lab_energy)
    dict = {'labid': lab_name,
        lab_name+'-number': fh_opens,
        lab_name+'-current-kw': str(round(lab_energy, 2)) + ' kW',
        lab_name+'-today-kwh': str(round(lab_energy*500, 2)) + ' kWh',
        lab_name+'-temperature': str(round(random.uniform(71,72))) + ' °F',
        lab_name+'-fumehood-energy-ratio': lab_ratios[lab_name],
        lab_name+'-occ' : occ,
        lab_name+'-ave-nrg': str(round(lab_energy*1.10002, 2)) + ' kWh',
        lab_name+'-nrg-trend': lab_compares[lab_name],
        'fumehoods': []}
    dict['fumehoods'] = fh_cons
    return dict

if __name__ == '__main__':
    lab_info('rabinowitz_icahn_201')
