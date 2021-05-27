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
    if not (index >= 0 and index < 15):
        return result
    
    views = [
        "vulgard",
        "polarity",
        "subjectivity",

        "covid",
        "covid_subjectivity",
        "covid_polarity",

        "climate",
        "climate_subjectivity",
        "climate_polarity",

        "finance",
        "finance_subjectivity",
        "finance_polarity",

        "housing",
        "housing_subjectivity",
        "housing_polarity",
    ]

    descriptions = [
        "The amount of swear words comparing to the number of bachelor degree graduates.",
        "The polarity of tweets comparing to the median sales price of houses for the last 12 months.",
        "The subjectivity of tweets.",

        "The covid (and related words) word count comparing to Seifa Index Of Relative Socio-Economic Disadvantage 2016 Index Score.",
        "Covid tweets' subjectivity comparing to the socio-economic disadvantage index score.",
        "Covid tweets' polarity comparing to the socio-economic disadvantage index score.",

        "The climate (and related words) word count comparing to the number of bachelor degree graduates.",
        "Climate tweets' subjectivity comparing to the the number of bachelor degree graduates.",
        "Climate tweets' polarity comparing to the the number of bachelor degree graduates.",

        "The finance (and related words) word count comparing to Seifa Index Of Relative Socio-Economic Disadvantage 2016 Index Score.",
        "Finance tweets' subjectivity comparing to the socio-economic disadvantage index score.",
        "Finance tweets' polarity comparing to the socio-economic disadvantage index score.",

        "The housing (and related words) word count comparing to the number of bachelor degree graduates.",
        "Housing tweets' subjectivity comparing to the the number of bachelor degree graduates.",
        "Housing tweets' polarity comparing to the the number of bachelor degree graduates."
    ]

    titles = [
        "Vulgard vs Education",
        "Polarity vs Housing",
        "Subjectivity",

        "Covid vs Social Economics",
        "Covid Subjectivity vs Social Economics",
        "Covid Polarity vs Social Economics",

        "Climate vs Education",
        "Climate Subjectivity vs Education",
        "Climate Polarity vs Education",

        "Finance vs Social Economics",
        "Finance Subjectivity vs Social Economics",
        "Finance Polarity vs Social Economics",

        "Housing vs Education",
        "Housing Subjectivity vs Education",
        "Housing Polarity vs Education",
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
        "covid_subjectivity": "social",
        "covid_polarity": "social",

        "climate": "education",
        "climate_subjectivity": "education",
        "climate_polarity": "education",

        "finance": "social",
        "finance_subjectivity": "social",
        "finance_polarity": "social",

        "housing": "education",
        "housing_subjectivity": "education",
        "housing_polarity": "education",
    }


    view_result = db.get_stats(views[index])
    print(view_result)

    counter_key = "count"

    if "covid" in views[index]:
        counter_key = "covid_counter"
    elif "climate" in views[index]:
        counter_key = "climate_counter"
    elif "finance" in views[index]:
        counter_key = "finance_counter"
    elif "housing" in views[index]:
        counter_key = "housing_counter"

    count_result = db.get_stats(counter_key);
    print(count_result)
    

    compensation = 100

    if views[index]  == "subjectivity" \
        or views[index] == "covid_subjectivity" \
        or views[index] == "climate_subjectivity" \
        or views[index] == "finance_subjectivity" \
            or views[index] == "housing_subjectivity":
        compensation = 1
   

    result = {
        "sydney": {
            "aurin": aurin[data_pairing[views[index]]]["sydney_1"],
            "score": round((view_result["sydney_1"] + view_result["sydney_2"]) / (count_result["sydney_1"] + count_result["sydney_2"]) * compensation, 5),
            "label": "Sydney"
        },
        "melbourne": {
            "aurin": aurin[data_pairing[views[index]]]["melbourne_1"],
            "score": round((view_result["melbourne_1"] + view_result["melbourne_2"]) / (count_result["melbourne_1"] + count_result["melbourne_2"]) * compensation, 5),
            "label": "Melbourne"
        },
        "data_name": views[index],
        "description": descriptions[index],
        "title": titles[index]
    }

    return json.dumps(result)

