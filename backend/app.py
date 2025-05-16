from flask import Flask, jsonify, render_template
from datetime import datetime
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')

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

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)