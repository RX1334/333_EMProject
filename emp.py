from flask import Flask, make_response, request
from flask import render_template
from database import get_fumehood_output
import random
# ----------------------------------------------------------------------

app = Flask(__name__, template_folder='./templates', static_folder='./static')
# app = Flask(__name__, template_folder='.')

# ----------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------
# @app.route('/', methods=['GET'])
# def index():
#     # fumehoods_usage = get_fumehood_output()
#     # if fumehoods_usage is None:
#     #     fumehoods_usage = ['OFF', 'OFF', 'OFF', 'OFF']
#     # key val pairs are fumehood_id and their energy use
#     fumehoods_usage = {}
#     for i in range(4):
#         fumehoods_usage[i] = random.randint(100, 200)
#     # html = render_template('index.html', fumehoods_usage=fumehoods_usage)
#     html = render_template('master_template.html')
#     response = make_response(html)
#     return response

@app.route('/', methods=['GET'])
def lab_summaries():
    # compiles widgets
    dashboard_content = render_template('header-widget-2.html')
    dashboard_content += render_template('lab-summary-widget.html', lab_name='rabinowitz_icahn_201')
    dashboard_content += render_template('lab-summary-widget.html')

    # renders dashboard with those widgets
    html = render_template('master_template.html', dashboard_content=dashboard_content)
    response = make_response(html)
    return(response)

# @app.route('/fumehood_stuff', methods=['GET'])
# def fumehood_stuff():


# arguments: fumehood_id, output: html of fumehood summary widgets
@app.route('/fumehood_summary', methods=['GET'])
def fumehood_summary():
    fumehoods_usage = {}
    for i in range(4):
        fumehoods_usage[i] = random.randint(100, 200)
    # return fumehoods_usage
    fumehood_id = request.args.get('fumehood_id')

    # Error handling
    if not fumehood_id:
        html = ''
        response = make_response(html)
        return response
    dashboard_content = render_template('header-widget-2.html')
    dashboard_content += render_template('fumehood-summary-widget.html')
    dashboard_content += render_template('fumehood-summary-widget.html')

    # renders dashboard with those widgets
    html = render_template('master_template.html', dashboard_content=dashboard_content)
    response = make_response(html)
    return(response)


# Args: Lab name
# Output: HTML of Lab sum page w/ energy-consump-widget, power-consump-widget,
# graph widget,
@app.route('/lab_summary', methods=['GET'])
def lab_summary():
    # Get the lab that's requested, use it to get the info
    lab_name = request.args.get('lab_name')
    if not lab_name:
        # Come up with a better way to do error handling later, for now just return
        # empty string
        html = ''
        response = make_response(html)
        return response

    # Here is where we'd use the lab name to fetch data from the database, but
    # since that's not setup yet, we're giving some dummy data instead.

    # First do the widg container for power and energy consump
    dashboard_content = render_template('header-widget-2.html')
    dashboard_content += '<div class="consumption-widget-container widget-container">'
    dashboard_content += render_template('energy-consumption-widget.html')
    dashboard_content += render_template('power-consumption-widget.html')
    dashboard_content += '</div>'

    # Next, do the moving day average widget
    dashboard_content += render_template('barchart-widget.html')

    # Next, include the fumehood widgets (let's please limit it to 4 fumehoods per page)
    num_fumehoods = 4 # This should be data fetched from the database
    # fumehoods_usage = {}
    # for i in range(num_fumehoods):
    #     fumehoods_usage[i] = random.randint(100, 200)
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
    if lab_name:
        # Here, get the relevant data given a lab_name.
        # For now, we just use dummy data.
        data_dict[lab_name + '-number'] = random.randint(0, 4)
        data_dict[lab_name + '-current-kw'] = round(random.uniform(0.5,1.5), 2)
        data_dict[lab_name + '-today-kwh'] = round(random.uniform(2,4), 2)
    if fumehood_id:
        # We get the relevant data given an id
        data_dict[fumehood_id + '_cur_power'] = round(random.uniform(0.5,1.5), 2)
        data_dict[fumehood_id + '_today_consump'] = round(random.uniform(2,4), 2)
        data_dict[fumehood_id + '_hours_today'] = random.randint(0, 4)
        data_dict[fumehood_id + '_ave_hours'] = round(random.uniform(2,4), 2)
    return data_dict