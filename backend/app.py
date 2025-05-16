from flask import Flask, jsonify
from datetime import datetime
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

@app.route("/dashboard")
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

        # Process results
        formatted_data = []
        for item in data.get('hydra:member', []):
            # Format emission factor to 3 decimal places
            ef = round(item.get('emissionfactor', 0), 3)
            
            # Parse and format timestamps
            valid_from = datetime.fromisoformat(item['validfrom'])
            valid_to = datetime.fromisoformat(item['validto'])
            
            # Format time range with 24:00 for midnight
            from_time = valid_from.strftime("%H:%M")
            to_hour = valid_to.hour
            to_time = "24:00" if to_hour == 0 else f"{to_hour:02}:00"

            formatted_data.append({
                'emission_factor': ef,
                'time_range': f"{from_time} - {to_time}"
            })

        return jsonify(formatted_data)

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"API request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)