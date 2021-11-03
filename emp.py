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
    html = render_template('index.html', fumehoods_usage=[fumehoods_usage[0][0], fumehoods_usage[1][0], fumehoods_usage[2][0], fumehoods_usage[3][0]])
    response = make_response(html)
    return response
