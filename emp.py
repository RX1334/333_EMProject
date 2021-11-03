from flask import Flask, make_response
from flask import render_template
from database import get_fumehood_output
import random
# ----------------------------------------------------------------------

app = Flask(__name__, template_folder='./templates', static_folder='./static')
# app = Flask(__name__, template_folder='.')

# ----------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------
@app.route('/', methods=['GET'])
def index():
    # fumehoods_usage = get_fumehood_output()
    # if fumehoods_usage is None:
    #     fumehoods_usage = ['OFF', 'OFF', 'OFF', 'OFF']
    # key val pairs are fumehood_id and their energy use
    fumehoods_usage = {}
    for i in range(4):
        fumehoods_usage[i] = random.randint(100, 200)
    html = render_template('index.html', fumehoods_usage=fumehoods_usage)
    response = make_response(html)
    return response

@app.route('/fumehood_stuff', methods=['GET'])
def fumehood_stuff():
    fumehoods_usage = {}
    for i in range(4):
        fumehoods_usage[i] = random.randint(100, 200)
    return fumehoods_usage