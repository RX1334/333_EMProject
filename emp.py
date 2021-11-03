from flask import Flask, make_response
from flask import render_template
from database import get_fumehood_output
# ----------------------------------------------------------------------

app = Flask(__name__, template_folder='./templates', static_folder='./static')
# app = Flask(__name__, template_folder='.')

# ----------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------
@app.route('/', methods=['GET'])
def index():
    fumehoods_usage = get_fumehood_output()
    if fumehoods_usage is None:
        fumehoods_usage = ['OFF', 'OFF', 'OFF', 'OFF']
    html = render_template('index.html', fumehoods_usage=fumehoods_usage)
    response = make_response(html)
    return response
