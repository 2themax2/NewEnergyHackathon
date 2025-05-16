from flask import Flask
import requests
from dotenv import load_dotenv
import os
import json
app = Flask(__name__)


load_dotenv()

@app.route("/")
def home():
    return "default"



@app.route("/dashboard")
def hello_there():


    url = "https://api.ned.nl/v1/utilizations"

    headers = {
    'X-AUTH-TOKEN': os.getenv('api'),
    'accept': 'application/ld+json'}
    params = {'point': 0, 'type': 27, 'granularity': 5, 'granularitytimezone': 1, 'classification': 1, 'activity': 1,
    'validfrom[strictly_before]': '2025-05-18', 'validfrom[after]': '2025-05-16'}
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)

    for item in response:
        print(item)
        print('\n')

    return str(response)