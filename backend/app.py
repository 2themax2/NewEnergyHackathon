from flask import Flask, jsonify, render_template, request
from datetime import datetime, timezone
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

app_data = {
    'car_charging_hours': 5,
    'hard_charge_end_time': '07:00'
}

def best_time_slots(data, num_slots_to_pick):
    if not data or num_slots_to_pick <= 0:
        return []
    sorted_data_by_emission = sorted(data, key=lambda x: x['height'])
    best_emission_slots = sorted_data_by_emission[:int(num_slots_to_pick)]
    chronological_best_slots = sorted(best_emission_slots, key=lambda x: x['label'])
    return chronological_best_slots


@app.route("/dashboard")
@app.route('/')
def home():
    return render_template('index.html')

@app.route("/dashboard/data")
def get_utilization_data():
    try:
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
        response.raise_for_status()
        data = response.json()

        bar_data = []
        slot_duration_minutes = 5

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
                    bar_data.append({'height': height, 'label': ''})

        latest_ef = round(data['hydra:member'][-1].get('emissionfactor', 0), 3) if data.get('hydra:member') else 0

        best_charging_slots = best_time_slots(bar_data[6:30], app_data.get('car_charging_hours', 0))

        return jsonify({
            'bar_data': bar_data,
            'latest_ef': latest_ef,
            'car_charging_hours': app_data.get('car_charging_hours'),
            'hard_charge_end_time': app_data.get('hard_charge_end_time'),
            'best_charging_slots': best_charging_slots
        })

    except requests.exceptions.RequestException as e:
        print(f"API request failed: {str(e)}")
        return jsonify({"error": f"API request failed: {str(e)}"}), 500
    except Exception as e:
        print(f"An error occurred in get_utilization_data: {str(e)}")
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

@app.route('/set_car_hours', methods=['POST'])
def set_car_hours():
    try:
        data = request.get_json()
        hours = data.get('hours')

        if hours is None:
            return jsonify({"error": "Missing 'hours' value."}), 400
        try:
            hours_float = float(hours)
            if hours_float < 0:
                return jsonify({"error": "Invalid 'hours' value. Must be a non-negative number."}), 400
        except ValueError:
            return jsonify({"error": "Invalid 'hours' value. Must be a number."}), 400


        app_data['car_charging_hours'] = hours_float
        print(f"Car charging hours set to: {app_data['car_charging_hours']}")
        return jsonify({"message": "Car charging hours updated successfully.", "current_hours": app_data['car_charging_hours']}), 200
    except Exception as e:
        print(f"Error in /set_car_hours: {str(e)}")
        return jsonify({"error": "An internal error occurred."}), 500

@app.route('/set_hard_charge_end_time', methods=['POST'])
def set_hard_charge_end_time():
    try:
        data = request.get_json()
        time_value = data.get('time')

        if not time_value:
            return jsonify({"error": "Invalid or missing 'time' value."}), 400

        app_data['hard_charge_end_time'] = time_value
        print(f"Hard charge end time set to: {app_data['hard_charge_end_time']}")
        return jsonify({"message": "Hard charge end time updated successfully.", "current_time": app_data['hard_charge_end_time']}), 200
    except Exception as e:
        print(f"Error in /set_hard_charge_end_time: {str(e)}")
        return jsonify({"error": "An internal error occurred."}), 500


if __name__ == '__main__':
    app.run(debug=True)