from flask import Flask, make_response, request
from flask import render_template
from database import get_fumehood_output
import random
# ----------------------------------------------------------------------

app = Flask(__name__, template_folder='./templates', static_folder='./static')

# ----------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------

@app.route('/', methods=['GET'])
def lab_summaries():
    # compiles widgets
    dashboard_content = render_template('header-widget-2.html', page_name='Lab Dashboard')
    dashboard_content += render_template('lab-summary-widget.html', lab_name='rabinowitz_icahn_201')
    # dashboard_content += render_template('lab-summary-widget.html')

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

    dashboard_content = render_template('header-widget-2.html', page_name=fumehood_id)
    dashboard_content += render_template('fumehood-summary-widget.html', fumehood_id=fumehood_id)
    dashboard_content += render_template('barchart-widget.html')

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
    dashboard_content = render_template('header-widget-2.html', page_name=lab_name)
    dashboard_content += '<div class="consumption-widget-container widget-container">'
    dashboard_content += render_template('energy-consumption-widget.html', lab_name=lab_name)
    dashboard_content += render_template('power-consumption-widget.html', lab_name=lab_name)
    dashboard_content += '</div>'

    # moving day average widget
    dashboard_content += render_template('barchart-widget.html')

    # include the fumehood widgets
    num_fumehoods = 4 # This should be data fetched from the database
    fumehoods_usage = ['OFF', 123, 123, 123]
    dashboard_content += '<div class="fume-hood-widget-container widget-container">'
    for i in range(num_fumehoods):
        fumehood_name = "Fume Hood #" + str(i + 1)
        fumehood_id = "fumehood" + str(i)
        dashboard_content += '<span>'
        dashboard_content += render_template('mini-fume-hood-widget.html', fumehood_usage=fumehoods_usage[i], fumehood_id=fumehood_id)
        dashboard_content += '</span>'
    dashboard_content += '</div>'

    # renders dashboard with those widgets
    html = render_template('master_template.html', dashboard_content=dashboard_content)
    response = make_response(html)
    return(response)


# Temporary function for fetching all the relevant
# real-time data given either a lab name or a fumehood id
# args: optional for either lab_name or fumehood_id (if neither provided,
#       just return None)
# rets: dictionary of key val pairs, where it returns all the necessary data to update
#       key=smth so the front end knows what jquery to do (ideally it's just the tag id)
#       val=the data value attached to this pointd
@app.route('/real_time_data', methods=['GET'])
def real_time_data():
    # We assume just one lab_name is being requested; if there are multiple labs that
    # need their data updated at once, call this func mult times
    lab_name = request.args.get('lab_name')
    fumehood_id = request.args.get('fumehood_id')
    data_dict = {}
    print(fumehood_id)
    if lab_name:
        # Here, get the relevant data given a lab_name.
        # For now, we just use dummy data.
        data_dict[lab_name + '-number'] = str(random.randint(0, 4)) +  ' of 4'
        data_dict[lab_name + '-current-kw'] = str(round(random.uniform(0.5,1.5), 2)) + ' kW'
        data_dict[lab_name + '-today-kwh'] = str(round(random.uniform(2,4), 2)) + ' kWh'
    # if fumehood_id:
    #     # We get the relevant data given an id
    #     data_dict[fumehood_id + '-kw'] = str(round(random.uniform(0.5,1.5), 2)) + ' kW'
    #     data_dict[fumehood_id + '-kwh'] = str(round(random.uniform(2,4), 2)) + ' kWh'
    #     data_dict[fumehood_id + '-today'] = str(random.randint(0, 4)) + ' Hrs'
    #     data_dict[fumehood_id + '-avg-day'] = str(round(random.uniform(2,4), 2)) + ' Hrs'
    #     data_dict[fumehood_id + '-status'] = 'CLOSED' if random.uniform(0, 1) > 0.5 else 'OPEN'
    #     data_dict[fumehood_id + '-mini-status'] = 'CLOSED' if random.uniform(0, 1) > 0.5 else 'OPEN'

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

    return data_dict