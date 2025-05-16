from flask import Flask, render_template, jsonify, request
from datetime import datetime
import requests

app = Flask(__name__, template_folder='templates')

power_state = False
connected_device = False
time_connected = None

def get_power_state():
    """Retrieve the power socket's power state"""
    return power_state


def set_power_state(on: bool):
    """Set the power socket's power state to the given boolean"""
    global power_state
    power_state = on


def get_connected_device():
    """Retrieves whether a device is currently connected to the power socket."""
    global connected_device
    return connected_device


def set_connected_device(connected: bool):
    """Sets whether a device is currently connected to the power socket."""
    global connected_device, time_connected
    connected_device = connected
    if connected:
        time_connected = datetime.now().hour
    else:
        time_connected = None


@app.route('/')
def home():
    """Render the home page containing the mockup socket"""
    return render_template('home.html')


@app.route('/api/power', methods=['GET'])
def api_get_power():
    """Retrieve the power socket's power state."""
    return jsonify({"on": get_power_state()})


@app.route('/api/power', methods=['POST'])
def api_set_power():
    """Set the power socket's power state to the given boolean, persist to database"""
    data = request.get_json(silent=True) or {}
    new_state = data['on']
    set_power_state(new_state)
    return jsonify({'on': new_state})


@app.route('/api/device', methods=['GET'])
def api_get_device_connected():
    """Retrieve whether a device is currently connected to the power socket."""
    return jsonify(
        {
            "device_connected": get_connected_device(),
            "time_connected": time_connected
        }
    )


@app.route('/api/device', methods=['POST'])
def api_set_device_connected():
    """Set whether a device is currently connected to the power socket, persist to database"""
    data = request.get_json(silent=True) or {}
    new_state = data['device_connected']
    set_connected_device(new_state)
    return jsonify({'device_connected': new_state})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
