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
    html = render_template('index.html')
    response = make_response(html)
    return response
