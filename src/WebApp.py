import os

from flask import Flask, render_template, jsonify

app = Flask(__name__, template_folder='../templates')
state = False


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/toggle', methods=['POST'])
def toggle():
    global state
    state = not state
    print(f'State: {state}')
    return jsonify(state=state)


if __name__ == '__main__':
    app.run(debug=True)
