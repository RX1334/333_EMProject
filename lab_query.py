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

def occupancy(root_url, token):
    occ_w = "System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-cscs-apog305.Local_IO.B47_RML210_OS1;"
    occ_e = "System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-csc-apog306.Local_IO.B47_RML210_OS2;"
    occ_req1 = requests.get(root_url + occ_w, headers={'Authorization': 'Bearer ' + token}, verify=False)
    occ_req2 = requests.get(root_url + occ_e, headers={'Authorization': 'Bearer ' + token}, verify=False)
    # calculate total occupancy
    return(int((((occ_req1.json()['Properties'])[0])['Value'])['Value']) + int((((occ_req2.json()['Properties'])[0])['Value'])['Value']))

def fh_open(root_url, token):
    #fume hood percent open (proxy for on/off)
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
    lights_open = {'west': 0, 'east': 0}
    points = ["System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-cscs-apog305.Local_IO.B47_2FWL_LM1;",
    "System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-csc-apog306.Local_IO.B47_2FWL_LM2;"]
    output = []
    for point in points:
        output.append(requests.get(root_url + point, headers={'Authorization': 'Bearer ' + token}, verify=False))
    lights_open['west'] = (((output[0].json()['Properties'])[0])['Value'])['Value']
    lights_open['east'] = (((output[1].json()['Properties'])[0])['Value'])['Value']
    return lights_open

def climate_energy():
    '''returns approximate energy usage of climate control devices'''
    points = []
    return 0

def fh_consumption(root_url, token, fh_opens):
    fh_cons = {'fh5c': [0], 'fh5d': [0], 'fh6c': [0], 'fh6d':[0]}
    for fh in fh_opens.keys():
        if fh_opens[fh] == 'OPEN':
            fh_cons[fh][0] = 1
    fh_cons['fh5c'].append("System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-cscs-apog305.FLN_1.B47_FHET1-5C.EXH_FLOW;")
    fh_cons['fh6c'].append("System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-csc-apog306.FLN_1.B47_FHET1-6C.EXH_FLOW;")
    fh_cons['fh5d'].append("System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-csc-apog306.FLN_1.B47_FHET1-5D.EXH_FLOW;")
    fh_cons['fh6d'].append("System1.ManagementView:ManagementView.FieldNetworks.Research_BACnet.Hardware.mec-csc-apog306.FLN_1.B47_FHET1-6D.EXH_FLOW;")
    print(fh_cons)
    output = []
    for point in fh_cons.keys():
        if fh_cons[point][0] == 1:
            get = requests.get(root_url + fh_cons[point][1], headers={'Authorization': 'Bearer ' + token}, verify=False)
            fh_cons[point] = (((get.json()['Properties'])[0])['Value'])['Value']
        else:
            fh_cons[point] = 'OFF'
    print(fh_cons)
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


def main():
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
    fh_energy = energy_calc(fh_cons)

    dict = {'24 hr energy consumption': 1, 
        'current power consumption': fh_cons,
        'fumehoods in use' : fh_opens,
        'occupants' : occ,
        'lights' : light_opens,
        'energy moving average' : 5,
        'consumption trend' : 6,
        'fumehoods':[
        {'id':'FH5C', 'current consumption': fh_cons['fh5c'], 'daily consumption': 3, 'daily use': 4, 'average daily use': 5},
        {'id':'FH6C', 'current consumption': fh_cons['fh6c'], 'daily consumption': 3, 'daily use': 4, 'average daily use': 5},
        {'id': 'FH5D', 'current consumption': fh_cons['fh5d'], 'daily consumption': 3, 'daily use': 4, 'average daily use': 5},
        {'id': 'FH6D', 'current consumption': fh_cons['fh6d'], 'daily consumption': 3, 'daily use': 4, 'average daily use': 5}]
    }
    t2 = time.time()
    print(t2-t1)
    print(dict)

if __name__ == '__main__':
    main()
