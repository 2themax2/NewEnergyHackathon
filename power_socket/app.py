from flask import Flask, render_template, jsonify, request
import sqlite3
import threading
import json

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
        conn.execute("UPDATE power_state SET is_on = ? WHERE id = 1", (int(on), ))
        conn.commit()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/api/power', methods=['GET'])
def api_get_power():
    return jsonify({"on": get_power_state_db()})

@app.route('/api/power', methods=['POST'])
def api_set_power():
    data = request.get_json(silent=True) or {}
    new_state = data['on']
    set_power_state_db(new_state)
    return jsonify({'on': new_state})


if __name__ == '__main__':
    app.run(debug=True)
