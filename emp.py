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

@app.route('/fumehood_stuff', methods=['GET'])
def fumehood_stuff():
    fumehoods_usage = {}
    for i in range(4):
        fumehoods_usage[i] = random.randint(100, 200)
    return fumehoods_usage

# arguments: fumehood_id, output: html of fumehood summary widgets
@app.route('/fumehood_summary_page', methods=['GET'])
def fumehood_summary_page():
    fumehood_id = request.args.get('fumehood_id')

    # Error handling
    if not fumehood_id:
        html = ''
        response = make_response(html)
        return response

    html = render_template('fumehood-summary-widget.html')
    html += render_template('fumehood-summary-widget.html')
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
    dashboard_content += '<div class="widget-container">'
    dashboard_content += render_template('energy-consumption-widget.html')
    dashboard_content += render_template('power-consumption-widget.html')
    dashboard_content += '</div>'

    # Next, do the moving day average widget
    dashboard_content += render_template('barchart-widget.html')

    # renders dashboard with those widgets
    html = render_template('master_template.html', dashboard_content=dashboard_content)
    response = make_response(html)
    return(response)

    # Next, include the fumehood widgets (let's please limit it to 4 fumehoods per page)
    # html += '<div class="fume-hood-widget-container widget-container">'
    # num_fumehoods = 3 # This should be data fetched from the database
    # fumehoods_usage = {}
    # for i in range(num_fumehoods):
    #     fumehoods_usage[i] = random.randint(100, 200)
    # for i in range(num_fumehoods):
    #     fumehood_name = "Fume Hood #" + str(i + 1)
    #     fumehood_id = "fumehood" + str(i)
    #     html += '<span>'
    #     html += render_template('mini-fume-hood-widget.html')
    #     html += '</span>'
    # html += '</div>'

