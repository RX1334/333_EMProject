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

# disable https warning
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

CONVERSION_FACTOR = 24.4243395
BUSINESS_DAYS = 261.0
HOURS = 8.0
LAB_SIZE = 9000.0

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


def lab_info():
    t1 = time.time()
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
    lab_energy = lab_energy_calc(fh_cons, climate)
    temp = climate*10

    dict = {'rabinowitz_icahn_201-today-kwh': str(round(lab_energy*12.379, 2)) + ' kWh', 
        'rabinowitz_icahn_201-current-kw': str(round(lab_energy, 2)) + ' kW',
        'current lab temperature': temp,
        'fumehoods in use' : fh_opens,
        'occupants' : occ,
        'lights' : light_opens,
        'energy moving average': str(lab_energy*1.10002) + ' kWh',
        'fumehood energy ratio': '68% Fume Hood, 32% Other',
        'lab chart data': [
            {'1week':  {'labels': ['11/11','11/12','11/13','11/14','11/15','11/16','11/17'], 
            'values': [450.139, 423.239, 390.291, 320.120, 490.390, 419.329, 213.221]}}, 
            {'1month':  {'labels': ['10/20-10/27', '10/27-11/3', '11/3-11/10', '11/10-11/17'], 'values': [400.272, 402.002, 381.078, 392.219]}}, 
            {'6months': {'labels': ['5/2021', '6/2021', '7/2021', '8/2021', '9/2021', '10/2021'], 'values': [383.382, 392.229, 402.225, 410.202]}}, 
            {'1year':  {'labels': ['11/2020', '12/2020', '1/2021', '2/2021', '3/2021', '4/2021',
             '5/2021', '6/2021', '7/2021', '8/2021', '9/2021', '10/2021'], 'values': [402.208, 303.443, 412.239, 380.393, 390.202, 399.250,
             402.240, 379.992, 389.225, 394.293, 428.393, 402.922]}}
        ], 
        'fumehoods':[
        {'id':'FH5C', 'current consumption': str(fh_cons['fh5c']) + ' kWh', 'daily consumption': 3, 'daily use': 4, 'average daily use': 5},
        {'id':'FH6C', 'current consumption': str(fh_cons['fh6c']) + ' kWh', 'daily consumption': 3, 'daily use': 4, 'average daily use': 5},
        {'id': 'FH5D', 'current consumption': str(fh_cons['fh5d']) + ' kWh', 'daily consumption': 3, 'daily use': 4, 'average daily use': 5},
        {'id': 'FH6D', 'current consumption': str(fh_cons['fh6d']) + ' kWh', 'daily consumption': 3, 'daily use': 4, 'average daily use': 5}]
    }
    return dict

if __name__ == '__main__':
    lab_info()
