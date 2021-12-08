from flask import Flask, make_response, request, render_template
# from flask import redirect, url_for, session, abort
import requests
from database import get_fumehood_output
from lab_query import lab_info, graph_info, report_archive_dates, weekly_report
import json
import random
import urllib
# from urllib.request import urlopen
# from urllib.parse import quote
# from re import sub

# from keys import APP_SECRET_KEY

# ----------------------------------------------------------------------

app = Flask(__name__, template_folder='./templates', static_folder='./static')
# app.secret_key = APP_SECRET_KEY

# # ----------------------------------------------------------------------

# CAS_URL = 'https://fed.princeton.edu/cas/'

# # ----------------------------------------------------------------------

# # Return url after stripping out the "ticket" parameter that was
# # added by the CAS server.

# def strip_ticket(url):
#     if url is None:
#         return "something is badly wrong"
#     url = sub(r'ticket=[^&]*&?', '', url)
#     url = sub(r'\?&?$|&$', '', url)
#     return url

# # ----------------------------------------------------------------------

# # Validate a login ticket by contacting the CAS server. If
# # valid, return the user's username; otherwise, return None.

# def validate(ticket):
#     val_url = (CAS_URL + "validate"
#         + '?service=' + quote(strip_ticket(request.url))
#         + '&ticket=' + quote(ticket))
#     lines = []
#     with urlopen(val_url) as flo:
#         lines = flo.readlines()   # Should return 2 lines.
#     if len(lines) != 2:
#         return None
#     first_line = lines[0].decode('utf-8')
#     second_line = lines[1].decode('utf-8')
#     if not first_line.startswith('yes'):
#         return None
#     return second_line

# # ----------------------------------------------------------------------

# # Authenticate the remote user, and return the user's username.
# # Do not return unless the user is successfully authenticated.

# def authenticate():

#     # If the username is in the session, then the user was
#     # authenticated previously.  So return the username.
#     if 'username' in session:
#         return session.get('username')

#     # If the request does not contain a login ticket, then redirect
#     # the browser to the login page to get one.
#     ticket = request.args.get('ticket')
#     if ticket is None:
#         login_url = (CAS_URL + 'login?service=' + quote(request.url))
#         abort(redirect(login_url))

#     # If the login ticket is invalid, then redirect the browser
#     # to the login page to get a new one.
#     username = validate(ticket)
#     if username is None:
#         login_url = (CAS_URL + 'login?service='
#             + quote(strip_ticket(request.url)))
#         abort(redirect(login_url))

#     # The user is authenticated, so store the username in
#     # the session.
#     session['username'] = username
#     return username

# # ----------------------------------------------------------------------
# # Routes
# # ----------------------------------------------------------------------

# @app.route('/logout', methods=['GET'])
# def logout():

#     authenticate()

#     # Delete the user's username from the session.
#     session.pop('username')

#     # Logout, and redirect the browser to the index page.
#     logout_url = (CAS_URL +  'logout?service='
#         + quote(sub('logout', 'index', request.url)))
#     abort(redirect(logout_url))

@app.route('/', methods=['GET'])
def lab_summaries():

    # authenticate()

    # compiles widgets
    dashboard_content = render_template('header-widget.html', page_name='Lab Dashboard')
    dashboard_content += render_template('heading-label.html', text='Your Monitored Rooms')
    dashboard_content += '<div class="lab-summary-widget-container widget-container">'
    dashboard_content += render_template('lab-summary-widget.html', lab_id='rabinowitz_icahn_201', lab_name='Rabinowitz, Icahn 201')
    dashboard_content += render_template('lab-summary-widget.html', lab_id='rabinowitz_icahn_202', lab_name='Rabinowitz, Icahn 202')
    dashboard_content += '</div>'

    # renders dashboard with those widgets
    html = render_template('master_template.html', dashboard_content=dashboard_content)
    response = make_response(html)
    return(response)

# arguments: fumehood_id
# output: html of fumehood summary widgets
@app.route('/fumehood_summary', methods=['GET'])
def fumehood_summary():

    # authenticate()

    # return fumehoods_usage
    lab_id = request.args.get('lab_id')
    lab_name = request.args.get('lab_name')
    fumehood_id = request.args.get('fumehood_id')
    fumehood_name = request.args.get('fumehood_name')

    # Error handling
    if not fumehood_id:
        html = ''
        response = make_response(html)
        return response
    dashboard_content = render_template('header-widget.html', page_name=fumehood_name, back_arrow_link='/lab_summary?lab_id=' + lab_id + '&lab_name=' + lab_name)
    dashboard_content += render_template('heading-label.html', text='Statistics')
    dashboard_content += render_template('fumehood-summary-widget.html', fumehood_id=fumehood_id)
    dashboard_content += render_template('heading-label.html', text='Visualizations')
    dashboard_content += render_template('barchart-report.html',
                                         name=fumehood_name,
                                         lab_id=lab_id,
                                         type_of_graph='Energy Consumption Trend')

    # renders dashboard with those widgets
    html = render_template('master_template.html', dashboard_content=dashboard_content)
    response = make_response(html)
    return(response)

# arguments: lab_id
# output: HTML of lab sum page w/ energy, power, graph, fumehoods
@app.route('/lab_summary', methods=['GET'])
def lab_summary():

    # authenticate()

    # get lab_id
    lab_id = request.args.get('lab_id')
    lab_name = request.args.get('lab_name')

    # temp error handling
    if not lab_id:
        html = ''
        response = make_response(html)
        return response

    # render energy and power widgets
    dashboard_content = render_template('header-widget.html', page_name=lab_name, lab_id=lab_id)
    dashboard_content += render_template('heading-label.html', text='Statistics')
    dashboard_content += '<div class="consumption-widget-container widget-container">'
    dashboard_content += render_template('energy-consumption-widget.html', lab_id=lab_id)
    dashboard_content += render_template('power-consumption-widget.html', lab_id=lab_id)
    dashboard_content += '</div>'

    # include the fumehood widgets
    num_fumehoods = 4 # This should be data fetched from the database
    dashboard_content += '<div class="fume-hood-widget-container widget-container">'
    for i in range(num_fumehoods):
        fumehood_id = "fumehood" + str(i)
        dashboard_content += '<span>'
        dashboard_content += render_template('mini-fume-hood-widget.html', lab_id=lab_id, lab_name=lab_name, fumehood_id=fumehood_id)
        dashboard_content += '</span>'
    dashboard_content += '</div>'
    dashboard_content += '<div class="consumption-widget-container widget-container">'
    dashboard_content += render_template('energy-trend-widget.html', lab_id=lab_id)
    dashboard_content += render_template('temperature-occupancy-widget.html', lab_id=lab_id)
    dashboard_content += '</div>'

    # bar chart widget
    dashboard_content += render_template('heading-label.html', text='Visualizations')
    dashboard_content += render_template('barchart-widget-json.html', name=lab_name,
                                         lab_id=lab_id, type_of_graph='Energy Consumption Trend')

    # renders dashboard with those widgets
    html = render_template('master_template.html', dashboard_content=dashboard_content)
    response = make_response(html)
    return(response)

# report archive
@app.route('/report_archive', methods=['GET'])
def report_archive():

    # authenticate()
    icahn_201_name = 'Rabinowitz, Icahn 201'
    icahn_201_id = 'rabinowitz_icahn_201'
    dates_array = report_archive_dates(icahn_201_id)

    # render energy and power widgets
    dashboard_content = render_template('header-widget.html', page_name='Report Archive')
    dashboard_content += render_template('report-heading-label.html', lab_name=icahn_201_name, lab_id=icahn_201_id)
    dashboard_content += '<div class="report-widget-container widget-container">'
    i = 0
    for date in dates_array:
        if i < 3:
            dashboard_content += render_template('report-widget.html', lab_id=icahn_201_id, lab_name=icahn_201_name, report_date=date, report_date_stripped=date.replace('.', ''))
        else:
            dashboard_content += render_template('report-widget.html', lab_id=icahn_201_id, lab_name=icahn_201_name, report_date=date, report_date_stripped=date.replace('.', ''), hidden='true')
        i += 1
    dashboard_content += '</div>'

    # renders dashboard with those widgets
    html = render_template('master_template.html', dashboard_content=dashboard_content)
    response = make_response(html)
    return(response)

# # @app.route('/report_archive_data', methods=['GET'])
# def report_archive_dates(lab_id):
#     return ['10.31.21', '10.24.21', '10.17.21', '10.10.21', '10.03.21']
#     # return from report_archive_dates() in lab_query.py

# should be replaced by call to lab_query, don't delete, just comment out pls
# def weekly_report(lab_id, date):
#     ndate = float(date[:5])
#     return {
#     'date' : date,
#     'week' : ['11.2', '11.3', ...],
#     'this_week_energy_consumption' : '323.3 kWh',
#     'this_week_avg_power_consumption' : '421.23 kW',
#     'this_week_avg_fumehood_usage' : '6 hrs',
#     'energy_consumption_kwh_day' : [3.1, 3.3, 3.2, 3.7, 3.9, 4.2, 3.2],
#     'energy_consumption_dollars_day' : [7.68, 5.64, 9.00, 10.23, 11.21, 13.21, 9.81],
#     'energy_consumption_lb_co2_day' : [8.1, 7.6, 5.4, 2.1, 9.8, 6.7, 9.4]
#     }

# This gets the summary in the weekly report
@app.route('/weekly_report_summary', methods=['GET'])
def weekly_report_summary():
    date = request.args.get('date')
    # Ideally, this should call the database to get the relevant stored information.
    return {
        'lab-summary-today-kwh': '11037 kWh',
        'lab-summary-current-kw': '53 kWh',
        'lab-summary-number': '16 Hrs'
    }
    return weekly_report('1', date)

# the printed weekly report, DONT DELETE THIS OR THE PRINT FAILS
@app.route('/weekly_report', methods=['GET'])
def printed_weekly_report():

    # authenticate()

    lab_id = request.args.get('lab_id')
    lab_name = request.args.get('lab_name')
    date = request.args.get('date')
    data_dict = weekly_report(lab_id, date)

    html = render_template('printed-weekly-report.html', data_dict=data_dict, lab_name=lab_name)
    response = make_response(html)
    return response

# report
@app.route('/report', methods=['GET'])
def report():

    # authenticate()

    # get lab_id
    lab_id = request.args.get('lab_id')
    lab_name = request.args.get('lab_name')
    week_name = request.args.get('week_name')

    # temp error handling
    if not lab_id or not week_name:
        html = ''
        response = make_response(html)
        return response

    # forms email subject
    email_subject = lab_name + ' ' + week_name + ' Weekly Report'
    # forms email body
    weeks_data = weekly_report(lab_id, week_name)
    email_body = 'Weekly Report for ' + lab_name + ', ' + str(weeks_data['date']) + '%0D%0A%0D%0A'
    email_body += 'Total Energy Consumption: ' + str(weeks_data['this_week_energy_consumption']) + '%0D%0A'
    email_body += 'Average Power Consumption: ' + str(weeks_data['this_week_avg_power_consumption']) + '%0D%0A'
    email_body += 'Average Fumehood Usage: ' + str(weeks_data['this_week_avg_fumehood_usage']) + '%0D%0A%0D%0A'
    email_body += 'Energy Consumption by Day:%0D%0A'
    for i in range(7):
        email_body += str(weeks_data['week'][i]) + ': '
        email_body += str(weeks_data['energy_consumption_kwh_day'][i]) + ' kWh / '
        email_body += '$' + str(weeks_data['energy_consumption_dollars_day'][i]) + ' / '
        email_body += str(weeks_data['energy_consumption_lb_co2_day'][i]) + ' lb CO2%0D%0A'

    # compiles widgets
    dashboard_content = render_template('header-widget.html', page_name= lab_name + ', Week of ' + week_name + ' Report', back_arrow_link='/report_archive')
    dashboard_content += render_template('heading-label.html', text='Statistics')
    dashboard_content += render_template('weekly-lab-summary-widget.html', lab_id='rabinowitz_icahn_201')
    dashboard_content += render_template('heading-label.html', text='Visualizations')
    # dashboard_content += render_template('barchart-widget-json.html', name='PLACEHOLDER', lab_id='rabinowitz_icahn_201', type_of_graph='Energy Consumption Trend')
    dashboard_content += render_template('barchart-report.html', week_name=week_name, lab_id='rabinowitz_icahn_201', type_of_graph='Energy Consumption Trend')
    dashboard_content += render_template('email-print-report.html', lab_id=lab_id, report_date_stripped=week_name.replace('.', ''), report_date=week_name, email_subject=email_subject, email_body=email_body, lab_name=lab_name)

    # renders dashboard with those widgets
    html = render_template('master_template.html', dashboard_content=dashboard_content)
    response = make_response(html)
    return(response)

# Get Report Chart Data
@app.route('/report-chart-data', methods=['GET'])
def report_chart():

    # authenticate()

    date = request.args.get('date')
    # For now, use fake data, but should call a lab_query func instead
    report_dict = {
        'date' : '10.31.21',
        'week' : ['10.31', '11.1', '11.2', '11.3', '11.4', '11.5', '11.6'],
        'this_week_energy_consumption' : '323.3 kWh',
        'this_week_avg_power_consumption' : '421.23 kW',
        'this_week_avg_fumehood_usage' : '6 hrs',
        'energy_consumption_kwh_day' : [7, 9, 3, 5, 7, 2, 1],
        'energy_consumption_dollars_day' : [3, 3, 2, 3, 7, 4, 5],
        'energy_consumption_lb_co2_day' : [4, 7, 5, 9, 6, 3, 4]
    }
    return report_dict

# Fetch real-time data given a lab name and/or fumehood id
# args: optional for either lab_name or fumehood_id (if neither provided,
#       just return None)
# rets: dictionary of key val pairs, where it returns all the necessary data to update
#       key=smth so the front end knows what jquery to do (ideally it's just the tag id)
#       val=the data value attached to this pointd
@app.route('/real_time_data', methods=['GET'])
def real_time_data():

    # authenticate()

    # We assume just one lab_id is being requested
    # lab_id = request.args.get('lab_id')
    # fumehood_id = request.args.get('fumehood_id')
    # data_dict = {}
    # if lab_id:
    #     # Here, get the relevant data given a lab_id.
    #     # For now, we just use dummy data.
    #     data_dict[lab_id + '-number'] = str(random.randint(0, 4)) +  ' of 4'
    #     data_dict[lab_id + '-current-kw'] = str(round(random.uniform(0.5,1.5), 2)) + ' kW'
    #     data_dict[lab_id + '-today-kwh'] = str(round(random.uniform(2,4), 2)) + ' kWh'
    #     data_dict[lab_id + '-temperature'] = str(random.randint(70, 80)) + ' °F'
    #     randint = random.randint(70,90)
    #     data_dict[lab_id + '-fumehood-energy-ratio'] = str(randint) + '% Fume Hoods ' + str(100-randint) + '% Other'
    #     data_dict[lab_id + '-occ'] = str(random.randint(0, 150)) + '%'
    #     data_dict[lab_id + '-ave-nrg'] = str(round(random.uniform(0.5,1.5), 2)) + ' kWh'
    #     data_dict[lab_id + '-nrg-trend'] = str(random.randint(50, 150)) + '%'

    # # HARDCODED DATA, CHANGE LATER
    # for i in range(4):
    #     fumehood_id = 'fumehood' + str(i)
    #     # We get the relevant data given an id
    #     data_dict[fumehood_id + '-kw'] = str(round(random.uniform(0.5,1.5), 2)) + ' kW'
    #     data_dict[fumehood_id + '-kwh'] = str(round(random.uniform(2,4), 2)) + ' kWh'
    #     data_dict[fumehood_id + '-today'] = str(random.randint(0, 4)) + ' Hrs'
    #     data_dict[fumehood_id + '-avg-day'] = str(round(random.uniform(2,4), 2)) + ' Hrs'
    #     data_dict[fumehood_id + '-status'] = 'CLOSED' if random.uniform(0, 1) > 0.5 else 'OPEN'
    #     data_dict[fumehood_id + '-mini-status'] = 'CLOSED' if random.uniform(0, 1) > 0.5 else 'OPEN'
    #     data_dict[fumehood_id + '-chart-data'] = {
    #         'dates': {
    #         'labels': [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7],
    #         'time': [round(random.uniform(0.6,1.4), 2) for _ in range(7)],
    #         },
    #         'weeks': {
    #         'labels': ["10.1-10.7", "10.8-10.14", "10.15-10.22", "10.23-10.29"],
    #         'time': [round(random.uniform(1.5,10)) for _ in range(4)],
    #         },
    #         'sixMonths': {
    #         'labels': [4, 5, 6, 7, 8, 9],
    #         'time': [round(random.uniform(6,40)) for _ in range(6)],
    #         },
    #         'years': {
    #         'labels': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    #         'time': [round(random.uniform(6,40)) for _ in range(12)],
    #         },
    #     }

    # # Fake chart data
    # data_dict[lab_id + '-chart-data'] = {
    #     'dates': {
    #     'labels': [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7],
    #     'time': [round(random.uniform(6,14), 2) for _ in range(7)],
    #     },
    #     'weeks': {
    #     'labels': ["10.1-10.7", "10.8-10.14", "10.15-10.22", "10.23-10.29"],
    #     'time': [round(random.uniform(15,100)) for _ in range(4)],
    #     },
    #     'sixMonths': {
    #     'labels': [4, 5, 6, 7, 8, 9],
    #     'time': [round(random.uniform(60,400)) for _ in range(6)],
    #     },
    #     'years': {
    #     'labels': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
    #     'time': [round(random.uniform(60,400)) for _ in range(12)],
    #     },
    # }

    # return data_dict
    return lab_info('rabinowitz_icahn_201')

@app.route('/get_graph_info', methods=['GET'])
def get_graph_info():
    lab_id = request.args.get('lab_id')
    return graph_info(lab_id)