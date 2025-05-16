from flask import Flask, render_template, jsonify, request
import sqlite3
import threading

app = Flask(__name__, template_folder='templates')

DB_PATH = 'database/database.db'
DB_LOCK = threading.Lock()


def get_power_state_db():
    """Retrieve the power socket's power state from the database."""
    with DB_LOCK, sqlite3.connect(DB_PATH) as conn:
        cur = conn.execute("SELECT is_on FROM power_state WHERE id = 1")
        row = cur.fetchone()
        return bool(row[0])


def set_power_state_db(on: bool):
    """Set the power socket's power state to the given boolean, persist to database"""
    with DB_LOCK, sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE power_state SET is_on = ? WHERE id = 1", (int(on),))
        conn.commit()


def get_connected_device_db():
    """Retrieves whether a device is currently connected to the power socket."""
    with DB_LOCK, sqlite3.connect(DB_PATH) as conn:
        curr = conn.execute("SELECT device_connected FROM power_state WHERE id = 1")
        row = curr.fetchone()
        return bool(row[0])


def set_connected_device_db(connected: bool):
    """Sets whether a device is currently connected to the power socket."""
    with DB_LOCK, sqlite3.connect(DB_PATH) as conn:
        conn.execute("UPDATE power_state SET device_connected = ? WHERE id = 1", (int(connected),))
        conn.commit()


@app.route('/')
def home():
    """Render the home page containing the mockup socket"""
    return render_template('home.html')


@app.route('/api/power', methods=['GET'])
def api_get_power():
    """Retrieve the power socket's power state."""
    return jsonify({"on": get_power_state_db()})


@app.route('/api/power', methods=['POST'])
def api_set_power():
    """Set the power socket's power state to the given boolean, persist to database"""
    data = request.get_json(silent=True) or {}
    new_state = data['on']
    set_power_state_db(new_state)
    return jsonify({'on': new_state})


@app.route('/api/device', methods=['GET'])
def api_get_device_connected():
    """Retrieve whether a device is currently connected to the power socket."""
    return jsonify({"device_connected": get_connected_device_db()})


@app.route('/api/device', methods=['POST'])
def api_set_device_connected():
    """Set whether a device is currently connected to the power socket, persist to database"""
    data = request.get_json(silent=True) or {}
    new_state = data['device_connected']
    set_connected_device_db(new_state)
    return jsonify({'device_connected': new_state})


if __name__ == '__main__':
    app.run(debug=True)
