from flask import Flask, render_template
from pymongo import MongoClient
from datetime import datetime
import json

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def call():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.6.2"

    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    client = MongoClient(CONNECTION_STRING)

    # Create the database for our example (we will use the same database throu oghout the tutorial
    cursor = client['project1']['opportunites2'].aggregate([
        {
            '$sort': {
                'last_call': 1
            }
        }, {
            '$limit': 4
        }
    ])
    dt = datetime.now()
    ts = datetime.timestamp(dt)

    cursor = list(cursor)
    for i in cursor:
        # for char in ['Australian','Ltd','Pty', 'of', 'Australia', 'Services']:
        #     i['client'] = i['client'].replace(char,'').strip()
        client['project1']['opportunites2'].update_one({ '_id': i['_id'] }, { "$set": { 'last_call': int(ts) } })
        i.pop('_id', None)
        print(i)
    return json.dumps([dict(i) for i in cursor])

if __name__ == "__main__":
    app.run(debug=True)