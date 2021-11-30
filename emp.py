from flask import Flask, make_response, request, render_template
from database import get_fumehood_output
from lab_query import lab_info
import json
import random
# ----------------------------------------------------------------------

app = Flask(__name__, template_folder='./templates', static_folder='./static')

# ----------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------

@app.route('/', methods=['GET'])
def lab_summaries():
    # compiles widgets
    dashboard_content = render_template('header-widget.html', page_name='Lab Dashboard')
    dashboard_content += render_template('heading-label.html', text='Your Monitored Rooms')
    dashboard_content += render_template('lab-summary-widget.html', lab_name='rabinowitz_icahn_201')

    # renders dashboard with those widgets
    html = render_template('master_template.html', dashboard_content=dashboard_content)
    response = make_response(html)
    return(response)

# arguments: fumehood_id
# output: html of fumehood summary widgets
@app.route('/fumehood_summary', methods=['GET'])
def fumehood_summary():
    # return fumehoods_usage
    fumehood_id = request.args.get('fumehood_id')

    # Error handling
    if not fumehood_id:
        html = ''
        response = make_response(html)
        return response

    dashboard_content = render_template('header-widget.html', page_name=fumehood_id)
    dashboard_content += render_template('heading-label.html', text='Statistics')
    dashboard_content += render_template('fumehood-summary-widget.html', fumehood_id=fumehood_id)
    dashboard_content += render_template('heading-label.html', text='Visualizations')
    dashboard_content += render_template('barchart-widget-json.html',
                                         name=fumehood_id,
                                         lab_name='rabinowitz_icahn_201',
                                         type_of_graph='Energy Consumption Trend')

    # renders dashboard with those widgets
    html = render_template('master_template.html', dashboard_content=dashboard_content)
    response = make_response(html)
    return(response)


# arguments: lab_name
# output: HTML of lab sum page w/ energy, power, graph, fumehoods
@app.route('/lab_summary', methods=['GET'])
def lab_summary():
    # get lab_name
    lab_name = request.args.get('lab_name')

    # temp error handling
    if not lab_name:
        html = ''
        response = make_response(html)
        return response

    # render energy and power widgets
    dashboard_content = render_template('header-widget.html', page_name=lab_name, lab_name=lab_name)
    dashboard_content += render_template('heading-label.html', text='Statistics')
    dashboard_content += '<div class="consumption-widget-container widget-container">'
    dashboard_content += render_template('energy-consumption-widget.html', lab_name=lab_name)
    dashboard_content += render_template('power-consumption-widget.html', lab_name=lab_name)
    dashboard_content += '</div>'

    # include the fumehood widgets
    num_fumehoods = 4 # This should be data fetched from the database
    dashboard_content += '<div class="fume-hood-widget-container widget-container">'
    for i in range(num_fumehoods):
        fumehood_id = "fumehood" + str(i)
        dashboard_content += '<span>'
        dashboard_content += render_template('mini-fume-hood-widget.html', fumehood_id=fumehood_id)
        dashboard_content += '</span>'
    dashboard_content += '</div>'

    # bar chart widget
    dashboard_content += render_template('heading-label.html', text='Visualizations')
    dashboard_content += render_template('barchart-widget-json.html', name=lab_name,
                                         lab_name=lab_name, type_of_graph='Energy Consumption Trend')

    # renders dashboard with those widgets
    html = render_template('master_template.html', dashboard_content=dashboard_content)
    response = make_response(html)
    return(response)

# report archive
@app.route('/report_archive', methods=['GET'])
def report_archive():

    dates_array = report_archive_dates()

    # render energy and power widgets
    dashboard_content = render_template('header-widget.html', page_name='Report Archive')
    dashboard_content += render_template('report-heading-label.html', text='Icahn 201 Reports')
    dashboard_content += '<div class="report-widget-container widget-container">'
    for date in dates_array:
        dashboard_content += render_template('report-widget.html', lab_name='rabinowitz_icahn_201', report_date=date, report_date_stripped=date.replace('.', ''))
    dashboard_content += '</div>'

    # renders dashboard with those widgets
    html = render_template('master_template.html', dashboard_content=dashboard_content)
    response = make_response(html)
    return(response)

# report
@app.route('/report', methods=['GET'])
def report():
    # get lab_name
    lab_name = request.args.get('lab_name')
    week_name = request.args.get('week_name')

    # temp error handling
    if not lab_name or not week_name:
        html = ''
        response = make_response(html)
        return response

    # compiles widgets
    dashboard_content = render_template('header-widget.html', page_name='Week of ' + week_name + ' Report')
    dashboard_content += render_template('heading-label.html', text='Statistics')
    dashboard_content += render_template('weekly-lab-summary-widget.html', lab_name='rabinowitz_icahn_201')
    dashboard_content += render_template('heading-label.html', text='Visualizations')
    # dashboard_content += render_template('barchart-widget-json.html', name='PLACEHOLDER', lab_name='rabinowitz_icahn_201', type_of_graph='Energy Consumption Trend')
    dashboard_content += render_template('barchart-report.html', name=week_name.replace('.', ''), lab_name='rabinowitz_icahn_201', type_of_graph='Energy Consumption Trend')
    dashboard_content += render_template('email-print-report.html')

    # renders dashboard with those widgets
    html = render_template('master_template.html', dashboard_content=dashboard_content)
    response = make_response(html)
    return(response)

# Get Report Chart Data
@app.route('/report-chart-data', methods=['GET'])
def report_chart():
    date = request.args.get('date')
    # For now, use fake data, but should call a lab_query func instead
    report_dict = {
        'date' : '10.31.21',
        'week' : ['10.31', '11.1', '11.2', '11.3', '11.4', '11.5', '11.6'],
        'this_week_energy_consumption' : '323.3 kWh',
        'this_week_avg_power_consumption' : '421.23 kW',
        'this_week_avg_fumehood_usage' : '6 hrs',
        'energy_consumption_kwh_day' : [7, 9, 3,5 ,7, 2, 1],
        'energy_consumption_dollars_day' : [3, 3, 2, 3, 7, 4, 5],
        'energy_consumption_lb_co2_day' : [4, 7, 5, 9, 6, 3, 4]
    }
    return report_dict

# @app.route('/report_archive_data', methods=['GET'])
def report_archive_dates():
    return ['10.31.21', '10.24.21', '10.17.21', '10.10.21', '10.3.21']
    # return from report_archive_dates() in lab_query.py

@app.route('/weekly_report', methods=['GET'])
def weekly_report():
    date = request.args.get('date')
    data_dict = weekly_report(date)

    html = render_template('printed-weekly-report.html', data_dict=data_dict)
    response = make_response(html)
    return response


def weekly_report(date):
    return {
    'date' : date,
    'week' : ['10.31', '11.1', '11.2', '11.3', '11.4', '11.5', '11.6'],
    'this_week_energy_consumption' : '323.3 kWh',
    'this_week_avg_power_consumption' : '421.23 kW',
    'this_week_avg_fumehood_usage' : '6 hrs',
    'energy_consumption_kwh_day' : [3.1, 3.3, 3.2, 3.7, 3.9, 4.2, 3.2],
    'energy_consumption_dollars_day' : [7.68, 5.64, 9.00, 10.23, 11.21, 13.21, 9.81],
    'energy_consumption_lb_co2_day' : [8.1, 7.6, 5.4, 2.1, 9.8, 6.7, 9.4]
    }


# Temporary function for fetching all the relevant
# real-time data given either a lab name or a fumehood id
# args: optional for either lab_name or fumehood_id (if neither provided,
#       just return None)
# rets: dictionary of key val pairs, where it returns all the necessary data to update
#       key=smth so the front end knows what jquery to do (ideally it's just the tag id)
#       val=the data value attached to this pointd
@app.route('/real_time_data', methods=['GET'])
def real_time_data():
    # We assume just one lab_name is being requested
    lab_name = request.args.get('lab_name')
    fumehood_id = request.args.get('fumehood_id')
    data_dict = {}
    if lab_name:
        # Here, get the relevant data given a lab_name.
        # For now, we just use dummy data.
        data_dict[lab_name + '-number'] = str(random.randint(0, 4)) +  ' of 4'
        data_dict[lab_name + '-current-kw'] = str(round(random.uniform(0.5,1.5), 2)) + ' kW'
        data_dict[lab_name + '-today-kwh'] = str(round(random.uniform(2,4), 2)) + ' kWh'
        data_dict[lab_name + '-temperature'] = str(random.randint(70, 80)) + ' °F'
        randint = random.randint(70,90)
        data_dict[lab_name + '-fumehood-energy-ratio'] = str(randint) + '% Fume Hoods ' + str(100-randint) + '% Other'
        data_dict[lab_name + '-occ'] = str(random.randint(0, 150)) + '%'
        data_dict[lab_name + '-ave-nrg'] = str(round(random.uniform(0.5,1.5), 2)) + ' kWh'
        data_dict[lab_name + '-nrg-trend'] = str(random.randint(50, 150)) + '%'

    # HARDCODED DATA, CHANGE LATER
    for i in range(4):
        fumehood_id = 'fumehood' + str(i)
        # We get the relevant data given an id
        data_dict[fumehood_id + '-kw'] = str(round(random.uniform(0.5,1.5), 2)) + ' kW'
        data_dict[fumehood_id + '-kwh'] = str(round(random.uniform(2,4), 2)) + ' kWh'
        data_dict[fumehood_id + '-today'] = str(random.randint(0, 4)) + ' Hrs'
        data_dict[fumehood_id + '-avg-day'] = str(round(random.uniform(2,4), 2)) + ' Hrs'
        data_dict[fumehood_id + '-status'] = 'CLOSED' if random.uniform(0, 1) > 0.5 else 'OPEN'
        data_dict[fumehood_id + '-mini-status'] = 'CLOSED' if random.uniform(0, 1) > 0.5 else 'OPEN'
        data_dict[fumehood_id + '-chart-data'] = {
            'dates': {
            'labels': [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7],
            'time': [round(random.uniform(0.6,1.4), 2) for _ in range(7)],
            },
            'weeks': {
            'labels': ["10.1-10.7", "10.8-10.14", "10.15-10.22", "10.23-10.29"],
            'time': [round(random.uniform(1.5,10)) for _ in range(4)],
            },
            'sixMonths': {
            'labels': [4, 5, 6, 7, 8, 9],
            'time': [round(random.uniform(6,40)) for _ in range(6)],
            },
            'years': {
            'labels': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
            'time': [round(random.uniform(6,40)) for _ in range(12)],
            },
        }

    # Fake chart data
    data_dict[lab_name + '-chart-data'] = {
        'dates': {
        'labels': [1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7],
        'time': [round(random.uniform(6,14), 2) for _ in range(7)],
        },
        'weeks': {
        'labels': ["10.1-10.7", "10.8-10.14", "10.15-10.22", "10.23-10.29"],
        'time': [round(random.uniform(15,100)) for _ in range(4)],
        },
        'sixMonths': {
        'labels': [4, 5, 6, 7, 8, 9],
        'time': [round(random.uniform(60,400)) for _ in range(6)],
        },
        'years': {
        'labels': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
        'time': [round(random.uniform(60,400)) for _ in range(12)],
        },
    }

    # return data_dict
    return lab_info()