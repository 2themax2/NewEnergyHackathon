from flask import Flask
import requests
from dotenv import load_dotenv
import os
app = Flask(__name__)


load_dotenv()

@app.route("/")
def home():
    return "Hello, Flask!"



@app.route("/dashboard")
def hello_there():


    url = "https://api.ned.nl/v1/utilizations"

    headers = {
    'X-AUTH-TOKEN': os.getenv('api'),
    'accept': 'application/ld+json'}
    params = {'point': 0, 'type': 2, 'granularity': 3, 'granularitytimezone': 1, 'classification': 2, 'activity': 1,
    'validfrom[strictly_before]': '2020-11-17', 'validfrom[after]': '2020-11-16'}
    response = requests.get(url, headers=headers, params=params, allow_redirects=False)

    print(response.text)
    return str(response)