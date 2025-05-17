from flask import Flask, jsonify, render_template, request
from datetime import datetime, timezone
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

app_data = {
    'car_charging_hours': 5,
    'hard_charge_end_time': '04:00'
}

def best_time_slotsmin(data, num_slots_to_pick):
    if not data or num_slots_to_pick <= 0:
        return []
    sorted_data_by_emission = sorted(data, key=lambda x: x['height'])
    best_emission_slots = sorted_data_by_emission[:int(num_slots_to_pick)]
    chronological_best_slots = sorted(best_emission_slots, key=lambda x: x['label'])
    return chronological_best_slots


def best_time_slotsmax(data, num_slots_to_pick):
    if not data or num_slots_to_pick <= 0:
        return []
    sorted_data_by_emission = sorted(data, key=lambda x: x['height'])
    best_emission_slots = sorted_data_by_emission[-num_slots_to_pick:]
    chronological_best_slots = sorted(best_emission_slots, key=lambda x: x['label'])
    return chronological_best_slots

def get_socket_state():
    endpoint_url = "http://127.0.0.1:5001/api/device"
    try:
        # Make a GET request
        response = requests.get(endpoint_url)
        response.raise_for_status()  # Raise exception for HTTP errors
        data = response.json()
        return data.get("time_connected")

        # Or make a POST request with some data
        # response = requests.post(endpoint_url, json={"key": "value"})
        

    except requests.RequestException as e:
        print("fail")
        return

def post_power_state(power_state : bool):
    endpoint_url = "http://127.0.0.1:5001/api/power"
    try:
        # Make a GET request
        response = requests.post(endpoint_url, json= {"on" : power_state})


        # Or make a POST request with some data
        # response = requests.post(endpoint_url, json={"key": "value"})


    except requests.RequestException as e:
        print("fail")
        return

@app.route("/dashboard")
@app.route('/')
def home():
    get_socket_state()
    return render_template('index.html')

@app.route("/dashboard/koolstof")
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
            'validfrom[strictly_before]': '2025-05-19',
            'validfrom[after]': '2025-05-17'
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        bar_data = []
        slot_duration_minutes = 5

        if 'hydra:member' in data:
            for item in data['hydra:member']:
                ef = round(item.get('emissionfactor', 0), 3)
                height = ef * 1000
                valid_from = item.get('validfrom')
                valid_to = item.get('validto')

                if valid_from and valid_to:
                    from_hour = datetime.fromisoformat(valid_from).strftime('%H:%M')
                    to_hour = datetime.fromisoformat(valid_to).strftime('%H:%M')
                    bar_data.append({'height': height, 'label': f'{from_hour}-{to_hour}'})
                else:
                    bar_data.append({'height': height, 'label': ''})

        latest_ef = round(data['hydra:member'][-1].get('emissionfactor', 0), 3) if data.get('hydra:member') else 0

        socket_state = get_socket_state()
        power_state = False
        if socket_state != None:
            end_time = int(app_data.get('hard_charge_end_time', 0)[:2])
            if end_time == 4:
                dict_end_time = 0
            elif end_time == 3:
                dict_end_time = 1
            elif end_time == 2:
                dict_end_time = 2
            elif end_time == 1:
                dict_end_time = 3 
            elif end_time == 0:
                dict_end_time = 4
            elif end_time == 23:
                dict_end_time = 5
            elif end_time == 22:
                dict_end_time = 6
            elif end_time == 21:
                dict_end_time = 7
            elif end_time == 20:
                dict_end_time = 8
            elif end_time == 19:
                dict_end_time = 9
            elif end_time == 18:
                dict_end_time = 10
            elif end_time == 17:
                dict_end_time = 11
            elif end_time == 16:
                dict_end_time = 12
            elif end_time == 15:
                dict_end_time = 13
            elif end_time == 14:
                dict_end_time = 14
            elif end_time == 13:
                dict_end_time = 15
            elif end_time == 12:
                dict_end_time = 16
            elif end_time == 11:
                dict_end_time = 17
            elif end_time == 10:
                dict_end_time = 18
            elif end_time == 9:
                dict_end_time = 19
            elif end_time == 8:
                dict_end_time = 20
            elif end_time == 7:
                dict_end_time = 21
            elif end_time == 6:
                dict_end_time = 22
            elif end_time == 5:
                dict_end_time = 23
            else:
                dict_end_time = 24

            best_charging_slots = best_time_slotsmin(bar_data[(socket_state + 2): 30 - dict_end_time ], app_data.get('car_charging_hours', 0))
            for slot in best_charging_slots:
                if int(slot.get("label")[:2]) == socket_state:
                    power_state = True
        else: 
            best_charging_slots = None

        post_power_state(power_state)


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

@app.route("/dashboard/zon")
def get_utilization_data1():
    try:
        url = "https://api.ned.nl/v1/utilizations"
        headers = {'X-AUTH-TOKEN': os.getenv('api'), 'accept': 'application/ld+json'}
        params = {
            'point': 0,
            'type': 2,
            'granularity': 5,
            'granularitytimezone': 1,
            'classification': 1,
            'activity': 1,
            'validfrom[strictly_before]': '2025-05-19',
            'validfrom[after]': '2025-05-17'
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        bar_data = []
        slot_duration_minutes = 5

        if 'hydra:member' in data:
            for item in data['hydra:member']:
                ef = round(item.get('volume', 0), 3)
                height = ef / 1000000
                valid_from = item.get('validfrom')
                valid_to = item.get('validto')

                if valid_from and valid_to:
                    from_hour = datetime.fromisoformat(valid_from).strftime('%H:%M')
                    to_hour = datetime.fromisoformat(valid_to).strftime('%H:%M')
                    bar_data.append({'height': height, 'label': f'{from_hour}-{to_hour}'})
                else:
                    bar_data.append({'height': height, 'label': ''})

        latest_ef = round(data['hydra:member'][-1].get('volume', 0), 3) if data.get('hydra:member') else 0

        socket_state = get_socket_state()
        power_state = False
        if socket_state != None:
            end_time = int(app_data.get('hard_charge_end_time', 0)[:2])
            if end_time == 4:
                dict_end_time = 0
            elif end_time == 3:
                dict_end_time = 1
            elif end_time == 2:
                dict_end_time = 2
            elif end_time == 1:
                dict_end_time = 3 
            elif end_time == 0:
                dict_end_time = 4
            elif end_time == 23:
                dict_end_time = 5
            elif end_time == 22:
                dict_end_time = 6
            elif end_time == 21:
                dict_end_time = 7
            elif end_time == 20:
                dict_end_time = 8
            elif end_time == 19:
                dict_end_time = 9
            elif end_time == 18:
                dict_end_time = 10
            elif end_time == 17:
                dict_end_time = 11
            elif end_time == 16:
                dict_end_time = 12
            elif end_time == 15:
                dict_end_time = 13
            elif end_time == 14:
                dict_end_time = 14
            elif end_time == 13:
                dict_end_time = 15
            elif end_time == 12:
                dict_end_time = 16
            elif end_time == 11:
                dict_end_time = 17
            elif end_time == 10:
                dict_end_time = 18
            elif end_time == 9:
                dict_end_time = 19
            elif end_time == 8:
                dict_end_time = 20
            elif end_time == 7:
                dict_end_time = 21
            elif end_time == 6:
                dict_end_time = 22
            elif end_time == 5:
                dict_end_time = 23
            else:
                dict_end_time = 24

            best_charging_slots = best_time_slotsmax(bar_data[(socket_state + 2): 30 - dict_end_time ], app_data.get('car_charging_hours', 0))
            for slot in best_charging_slots:
                if int(slot.get("label")[:2]) == socket_state:
                    power_state = True
        else: 
            best_charging_slots = None

        post_power_state(power_state)


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

@app.route("/dashboard/load")
def get_utilization_data2():
    try:
        url = "https://api.ned.nl/v1/utilizations"
        headers = {'X-AUTH-TOKEN': os.getenv('api'), 'accept': 'application/ld+json'}
        params = {
            'point': 0,
            'type': 59,
            'granularity': 5,
            'granularitytimezone': 1,
            'classification': 1,
            'activity': 1,
            'validfrom[strictly_before]': '2025-05-10',
            'validfrom[after]': '2025-05-08'
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        bar_data = []
        slot_duration_minutes = 5

        if 'hydra:member' in data:
            for item in data['hydra:member']:
                ef = round(item.get('volume', 0), 3)
                height = ef /1000000
                valid_from = item.get('validfrom')
                valid_to = item.get('validto')

                if valid_from and valid_to:
                    from_hour = datetime.fromisoformat(valid_from).strftime('%H:%M')
                    to_hour = datetime.fromisoformat(valid_to).strftime('%H:%M')
                    bar_data.append({'height': height, 'label': f'{from_hour}-{to_hour}'})
                else:
                    bar_data.append({'height': height, 'label': ''})

        latest_ef = round(data['hydra:member'][-1].get('volume', 0), 4) if data.get('hydra:member') else 0

        socket_state = get_socket_state()
        power_state = False
        if socket_state != None:
            end_time = int(app_data.get('hard_charge_end_time', 0)[:2])
            if end_time == 4:
                dict_end_time = 0
            elif end_time == 3:
                dict_end_time = 1
            elif end_time == 2:
                dict_end_time = 2
            elif end_time == 1:
                dict_end_time = 3 
            elif end_time == 0:
                dict_end_time = 4
            elif end_time == 23:
                dict_end_time = 5
            elif end_time == 22:
                dict_end_time = 6
            elif end_time == 21:
                dict_end_time = 7
            elif end_time == 20:
                dict_end_time = 8
            elif end_time == 19:
                dict_end_time = 9
            elif end_time == 18:
                dict_end_time = 10
            elif end_time == 17:
                dict_end_time = 11
            elif end_time == 16:
                dict_end_time = 12
            elif end_time == 15:
                dict_end_time = 13
            elif end_time == 14:
                dict_end_time = 14
            elif end_time == 13:
                dict_end_time = 15
            elif end_time == 12:
                dict_end_time = 16
            elif end_time == 11:
                dict_end_time = 17
            elif end_time == 10:
                dict_end_time = 18
            elif end_time == 9:
                dict_end_time = 19
            elif end_time == 8:
                dict_end_time = 20
            elif end_time == 7:
                dict_end_time = 21
            elif end_time == 6:
                dict_end_time = 22
            elif end_time == 5:
                dict_end_time = 23
            else:
                dict_end_time = 24

            best_charging_slots = best_time_slotsmin(bar_data[(socket_state + 2): 30 - dict_end_time ], app_data.get('car_charging_hours', 0))
            for slot in best_charging_slots:
                if int(slot.get("label")[:2]) == socket_state:
                    power_state = True
        else: 
            best_charging_slots = None

        post_power_state(power_state)


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