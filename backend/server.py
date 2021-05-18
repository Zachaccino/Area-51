import couchdb
from flask import Flask
from flask_cors import CORS
import json


# Database Info
couch_user = "admin"
couch_password = "pass"
couch_address = "127.0.0.1"
couch_port = 5984
couch_db_name = "tweet"
couch_url = f'http://{couch_user}:{couch_password}@{couch_address}:{couch_port}/'

# Database
couch = couchdb.Server(couch_url)
db = couch['tweet']

# Server Info
server_version = 0.1
server_id = "SERVER-0"
app = Flask(__name__)
CORS(app)


dummy_text = "Curabitur at convallis augue, in iaculis ligula. Sed viverra mauris urna, ut aliquet ligula vulputate ut. Maecenas eu accumsan nisl. Nullam rhoncus lorem a ante placerat, sit amet tempus ipsum aliquet."

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
    result = {
        "sydney": {
            "aurin": [1, 2],
            "score": [10, 20],
            "labels": ["A1", "A2"]
        },
        "melbourne": {
            "aurin": [3, 4],
            "score": [30, 40],
            "labels": ["A3", "A4"]
        },
        "data_name": "sentiment",
        "description": "This is a description of the scenario. " + dummy_text,
        "title": "Scenario Title"
    }
    return json.dumps(result)

