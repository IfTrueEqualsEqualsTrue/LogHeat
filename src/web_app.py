from flask import Flask, render_template, jsonify, request

from backend import saver
from dynamic_plot import plot_manager
from utils import get_com_ports_json

app = Flask(__name__, template_folder='../templates', static_folder='../static')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/toggle', methods=['POST'])
def toggle():
    saver.toggle_saving()
    plot_manager.add_vertical_line()
    return jsonify(state=saver.is_saving)


@app.route('/update_com_port', methods=['POST'])
def update_com_port():
    data = request.get_json()
    print('setting reader')
    plot_manager.set_reader(data['port'])
    return jsonify(port=data['port'])


@app.route('/get_com_ports', methods=['GET'])
def get_com_ports():
    return get_com_ports_json()


@app.route('/plot_data', methods=['GET'])
def plot_data():
    return plot_manager.get_plot_json()
