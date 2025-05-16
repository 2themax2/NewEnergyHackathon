from flask import Flask
import requests
from dotenv import load_dotenv
import os
import json
app = Flask(__name__)

load_dotenv()

from flask import Flask, jsonify

@app.route("/dashboard")
def hello_there():
    url = "https://api.ned.nl/v1/utilizations"
    headers = {
        'X-AUTH-TOKEN': os.getenv('api'),
        'accept': 'application/ld+json'
    }
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
    results = []
    for item in data.get('hydra:member', []):
        results.append({
            'emissionfactor': item.get('emissionfactor'),
            'validfrom': item.get('validfrom'),
            'validto': item.get('validto')
        })
        
    print(results)
    return jsonify(results)