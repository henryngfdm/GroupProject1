from flask import Flask, render_template
from pymongo import MongoClient
import pandas as pd

app = Flask(__name__)

def get_database():
 
   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = "mongodb://127.0.0.1:27017/?directConnection=true&serverSelectionTimeoutMS=2000&appName=mongosh+1.6.2"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throu oghout the tutorial
   return client['project1']

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get")
def call():
    dbname = get_database()
    collection_name = dbname["opportunites"]
    item_details = collection_name.find()
    items_df = pd.DataFrame(item_details)
    items_df.replace({'NULL':"NA"}, inplace=True)
    items_df = items_df.drop(columns=['_id'])
    return items_df.head(4).to_json(force_ascii=True)

if __name__ == "__main__":
    app.run(debug=True)