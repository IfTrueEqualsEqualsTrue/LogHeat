from flask import Flask, render_template, jsonify, request

from Utils import get_com_ports_json

app = Flask(__name__, template_folder='../templates')
state = False
current_com_port = None


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/toggle', methods=['POST'])
def toggle():
    global state
    state = not state
    print(f'State: {state}')
    return jsonify(state=state)


@app.route('/update_com_port', methods=['POST'])
def update_com_port():
    global current_com_port
    data = request.get_json()
    current_com_port = data['port']
    print(f'COM Port updated to: {current_com_port}')
    return jsonify(port=current_com_port)


@app.route('/get_com_ports', methods=['GET'])
def get_com_ports():
    return get_com_ports_json()


if __name__ == '__main__':
    app.run(debug=True)
