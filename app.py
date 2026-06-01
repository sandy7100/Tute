from flask import Flask, request, render_template
from datetime import datetime
from dotenv import load_dotenv
import os 
import pymongo
import json

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')

client = pymongo.MongoClient(MONGO_URI)

db = client.test

collection = db['flask-tute']


#mongodb+srv://Sandeep:12345@flask.al3daju.mongodb.net/?appName=Flask
app = Flask(__name__)

@app.route('/')
def home():
    
    day_of_week = datetime.today().strftime('%A')
    current_time = datetime.now().strftime('%H:%M:%S')
    return render_template('index.html',day_of_week=day_of_week, current_time=current_time)
@app.route('/time')
def time():
   
    Current_time = datetime.now().strftime('%H:%M:%S')

    return Current_time

@app.route('/submit', methods=['POST'])
def submit():
    error = None 
    name = request.form.get("name", "").strip()
    password = request.form.get("password", "")
    # Validation
    if not name:
        error = "Name cannot be empty"
    elif not name.isalpha():
        error = "Name must contain only letters"
    if error:
        return render_template("index.html", error=error, name=name)
    
    # inseting into the database
    form_data = dict(request.form)
    collection.insert_one(form_data)
    return 'Data submitted successfully'

@app.route('/view')
def view():
    data = collection.find()

    data = list(data)
    for item in data:
        print(item)
        del item['_id']

    data = {
        'data':data
    }

    return data

def load_data():
    with open("data.json", "r") as file:
        data = json.load(file)
    return data

@app.route('/api')
def get_Data():
    data=load_data()
    return data


if __name__ == "__main__":
    app.run(debug=True)