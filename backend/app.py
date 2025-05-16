from flask import Flask, jsonify, render_template, request
from datetime import datetime, timezone
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

app_data = {
    'car_charging_hours': 1.0
}


def best_time_slots(data, hours):
    sorted_data = sorted(data, key=lambda x: x['emission_factor'])
    subset = sorted_data[:hours]
    sorted_data = sorted(subset, key=lambda x: x['time_range'])
    return sorted_data

def filter_time(data):


    return filterd_data


@app.route("/dashboard")
@app.route('/')
def home():
    return render_template('index.html')

@app.route("/dashboard/data")
def get_utilization_data():
    try:
        # API configuration
        url = "https://api.ned.nl/v1/utilizations"
        headers = {'X-AUTH-TOKEN': os.getenv('api'), 'accept': 'application/ld+json'}
        params = {
            'point': 0,
            'type': 27,
            'granularity': 5,
            'granularitytimezone': 1,
            'classification': 1,
            'activity': 1,
            'validfrom[strictly_before]': '2025-05-18',
            'validfrom[after]': '2025-05-16'
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status() # Will raise an HTTPError for bad responses (4XX or 5XX)
        data = response.json()

        bar_data = []
        if 'hydra:member' in data:
            for item in data['hydra:member']:
                ef = round(item.get('emissionfactor', 0), 3)
                height = ef
                valid_from = item.get('validfrom')
                valid_to = item.get('validto')

                if valid_from and valid_to:
                    from_hour = datetime.fromisoformat(valid_from).strftime('%H:%M')
                    to_hour = datetime.fromisoformat(valid_to).strftime('%H:%M')
                    bar_data.append({'height': height, 'label': f'{from_hour}-{to_hour}'})
                else:
                    bar_data.append({'height': height, 'label': ''}) # Or some other default label

        latest_ef = round(data['hydra:member'][-1].get('emissionfactor', 0), 3) if data.get('hydra:member') else 0

        return jsonify({'bar_data': bar_data, 'latest_ef': latest_ef})
        one = best_time_slots(formatted_data, 7)
        new = formatted_data[6:30]
        return jsonify(new)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API request failed: {str(e)}"}), 500
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/set_car_hours', methods=['POST'])
def set_car_hours():
    try:
        data = request.get_json()
        hours = data.get('hours')

        if hours is None or not isinstance(hours, (int, float)) or hours < 0:
            return jsonify({"error": "Invalid or missing 'hours' value. Must be a non-negative number."}), 400

        app_data['car_charging_hours'] = float(hours)
        print(f"Car charging hours set to: {app_data['car_charging_hours']}")
        return jsonify({"message": "Car charging hours updated successfully.", "current_hours": app_data['car_charging_hours']}), 200
    except Exception as e:
        print(f"Error in /set_car_hours: {str(e)}")
        return jsonify({"error": "An internal error occurred."}), 500


if __name__ == '__main__':
    app.run(debug=True)