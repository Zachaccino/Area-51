"""
Jingyuan Tu (1232404), Melbourne, Australia
Floyd Everest-Dobson (664751), Melbourne, Australia
Bradley Schuurman (586088), Melbourne, Australia
Iris Li (875195), Melbourne, Australia
Paul Ou (888653), Melbourne, Australia
"""

from flask import Flask
from flask_cors import CORS
import json
from TweetDatabase import TweetDatabase
import os
from flask import request


# Database Info
db_username = os.environ.get("DB_USERNAME")
db_password = os.environ.get("DB_PASSWORD")
db_address = os.environ.get("DB_ADDRESS")

db = TweetDatabase()
db.connect(db_username, db_password, db_address)
db.setup()


# Server Info
server_version = 0.1
server_id = "SERVER-0"
app = Flask(__name__)
CORS(app)


# Endpoints
@app.route('/')
def server_info():
    result = {
        "version": server_version,
        "id": server_id
    }
    return json.dumps(result)

@app.route('/data')
def data():
    # empty template
    result = {
        "sydney": {
            "aurin": 0,
            "score": 0,
            "labels": ["Sydney"]
        },
        "melbourne": {
            "aurin": 0,
            "score": 0,
            "labels": ["Melbourne"]
        },
        "data_name": "N/A",
        "description": "No scenario had been selected",
        "title": "N/A"
    }

    index = request.args.get('view_index')
    if not index.isnumeric():
        return result

    index = int(index)
    if not (index >= 0 and index < 9):
        return result
    
    views = [
        "vulgard",
        "polarity",
        "subjectivity",
        "count",
        "covid",
        "climate",
        "finance",
        "housing",
        "sport"
    ]

    descriptions = [
        "The amount of swear words comparing to the number of bachelor degree graduates.",
        "The polarity of tweets comparing to the median sales price of houses for the last 12 months.",
        "The subjectivity of tweets.",
        "The word count of tweets comparing to the number of bachelor degree graduates.",
        "The covid (and related words) word count comparing to Seifa Index Of Relative Socio-Economic Disadvantage 2016 Index Score.",
        "The climate (and related words) word count comparing to the number of bachelor degree graduates.",
        "The finance (and related words) word count comparing to Seifa Index Of Relative Socio-Economic Disadvantage 2016 Index Score.",
        "The housing (and related words) word count comparing to the number of bachelor degree graduates.",
        "Not Used"
    ]

    titles = [
        "Vulgard vs Education",
        "Polarity vs Housing",
        "Subjectivty",
        "Tweet Count vs Education",
        "Covid vs Social Economics",
        "Climate vs Education",
        "Finance vs Social Economics",
        "Housing vs Education",
        "Sports vs Social Economics"
    ]

    
    aurin = {
        # Index Score 2016
        "social": {
            "sydney_1": 35.95,
            "sydney_2": 35.95,
            "melbourne_1": 29.30,
            "melbourne_2": 29.30
        },
        # Medium sales price for the last 12 months
        "housing": {
            "sydney_1": 60682.22,
            "sydney_2": 60682.22,
            "melbourne_1": 28331.99,
            "melbourne_2": 28331.99
        },
        # Total BA Degress per LGA
        "education": {
            "sydney_1": 600.10,
            "sydney_2": 600.10,
            "melbourne_1": 577.42,
            "melbourne_2": 577.42
        },
        "none": {
            "sydney_1": 0,
            "sydney_2": 0,
            "melbourne_1": 0,
            "melbourne_2": 0
        }
    }

    data_pairing = {
        "vulgard": "education",
        "polarity": "housing",
        "subjectivity": "none",
        "count": "education",
        "covid": "social",
        "climate": "education",
        "finance": "social",
        "housing": "education",
        "sport": "social"
    }


    view_result = db.get_stats(views[index])
    count_result = db.get_stats("count");
   

    result = {
        "sydney": {
            "aurin": aurin[data_pairing[views[index]]]["sydney_1"],
            "score": round((view_result["sydney_1"] + view_result["sydney_2"]) / (count_result["sydney_1"] + count_result["sydney_2"]) * 100, 2),
            "label": "Sydney"
        },
        "melbourne": {
            "aurin": aurin[data_pairing[views[index]]]["melbourne_1"],
            "score": round((view_result["melbourne_1"] + view_result["melbourne_2"]) / (count_result["melbourne_1"] + count_result["melbourne_2"]) * 100, 2),
            "label": "Melbourne"
        },
        "data_name": views[index],
        "description": descriptions[index],
        "title": titles[index]
    }

    return json.dumps(result)

