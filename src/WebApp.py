from flask import Flask, render_template, jsonify, request
from Interface import backend
from Utils import get_com_ports_json

app = Flask(__name__, template_folder='../templates')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/toggle', methods=['POST'])
def toggle():
    backend.button_clicked()
    print(f'Saving state : {backend.plot_manager.csv_saver.is_saving}')
    return jsonify(state=backend.plot_manager.csv_saver.is_saving)


@app.route('/update_com_port', methods=['POST'])
def update_com_port():
    data = request.get_json()
    backend.update_com_port(data['port'])
    print(f'COM Port updated to: {data["port"]}')
    return jsonify(port=data['port'])


@app.route('/get_com_ports', methods=['GET'])
def get_com_ports():
    return get_com_ports_json()


if __name__ == '__main__':
    app.run(debug=True)
