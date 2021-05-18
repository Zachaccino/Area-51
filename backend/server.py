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

    titles = [
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

    # TODO: Need to add Aurin data which we don't have yet.
    aurin = {
        "sydney_1": 0,
        "sydney_2": 0,
        "melbourne_1": 0,
        "melbourne_2": 0
    }

    view_result = db.get_stats(views[index])

    # TODO: Need to compute results from two bounding boxes together.
    result = {
        "sydney": {
            "aurin": aurin["sydney_1"] + aurin["sydney_2"],
            "score": view_result["sydney_1"] + view_result["sydney_2"],
            "label": "Sydney"
        },
        "melbourne": {
            "aurin": aurin["melbourne_1"] + aurin["melbourne_2"],
            "score": view_result["melbourne_1"] + view_result["melbourne_2"],
            "label": "Melbourne"
        },
        "data_name": views[index],
        "description": descriptions[index],
        "title": titles[index]
    }

    return json.dumps(result)

