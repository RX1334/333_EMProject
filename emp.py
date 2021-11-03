from flask import Flask, make_response
from flask import render_template
# ----------------------------------------------------------------------

app = Flask(__name__, template_folder='./templates', static_folder='./static')
# app = Flask(__name__, template_folder='.')

# ----------------------------------------------------------------------
# Routes
# ----------------------------------------------------------------------
@app.route('/', methods=['GET'])
def index():
    fumehoods_usage = ['150', '10', '15', 'OFF']
    html = render_template('index.html', fumehoods_usage=fumehoods_usage)
    response = make_response(html)
    return response
