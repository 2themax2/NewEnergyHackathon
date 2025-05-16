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

        # Get data from API
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        # Process results for the bar chart
        bar_data = []
        if 'hydra:member' in data:
            num_items = len(data['hydra:member'])
            for i, item in enumerate(data['hydra:member']):
                ef = round(item.get('emissionfactor', 0), 3)
                # Basic scaling for the bar height (you might need to adjust this)
                height = ef * 100  # Example scaling
                bar_data.append({'height': height, 'label': f'{i+1}'})

        # Process results for the load information
        if data.get('hydra:member'):
            latest_data = data['hydra:member'][-1] # Assuming the last item is the most recent
            emission_factor = round(latest_data.get('emissionfactor', 0), 3)
        else:
            emission_factor = 0

        return jsonify({'bar_data': bar_data, 'latest_ef': emission_factor})

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)