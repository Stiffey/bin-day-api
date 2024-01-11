from datetime import datetime
from flask import Flask, send_from_directory, request, jsonify
from pathlib import Path
import json
import urllib.request, json
import os
import time
from collections import OrderedDict

from flask_cors import CORS

app = Flask(__name__)
app.debug = True
CORS(app)

def get_bin_details(url):
    with urllib.request.urlopen(url + '/bin_details.json') as f:
        return json.load(f)

def get_next_collection(collection_dict):
    current_date = datetime.now()
    for date_str in collection_dict.keys():
        date = datetime.strptime(date_str, '%d/%m/%Y')
        days_to_collection = date - current_date
        print(days_to_collection.days)
        if days_to_collection.days < 6 and days_to_collection.days >= 0:
            return date, collection_dict[date_str]
    return None, None

def get_bin_type(bin_collection):
    if 'Refuse Collection Service' in bin_collection:
        return "black"
    elif 'Recycling Collection Service' in bin_collection and 'Garden Waste Collection Service' not in bin_collection:
        return "blue"
    elif 'Garden Waste Collection Service' in bin_collection and 'Recycling Collection Service' not in bin_collection:
        return "brown"
    elif 'Recycling Collection Service' in bin_collection and 'Garden Waste Collection Service' in bin_collection:
        return "blue and brown"
    else:
        return "dunno"

@app.route('/')
def next_collection():
    url_root = request.url_root
    # return url_root
    collection_dict = get_bin_details(url_root)
    # return jsonify(collection_dict)
    next_collection_date, next_bin_collection = get_next_collection(collection_dict)
    next_bin_collection_type = get_bin_type(next_bin_collection)
    next_collection_date_formatted = next_collection_date.strftime("%A %d %B")

    path = 'app/bin_details.json'
    modification_time = os.path.getmtime(path)
    formatted_modification_time = time.ctime(modification_time)

    bin_collection_dict = {
        'date' : next_collection_date_formatted,
        'collecting' : next_bin_collection_type,
        'last_updated' : formatted_modification_time
    }

    return bin_collection_dict
    

@app.route('/all')
def bin_details():
    url_root = request.url_root
    bin_details = get_bin_details(url_root)
    collection_dict = []

    for date in bin_details.keys():
        date_obj = datetime.strptime(date, "%d/%m/%Y")
        if date_obj < datetime.now():
            continue
        formatted_date = date_obj.strftime("%Y/%m/%d")

        collection_dict.append({
            'date': formatted_date,
            'collecting': bin_details[date]
        })
    
    return collection_dict
    # sorted_collection_dict = OrderedDict(sorted(collection_dict.items(), key=lambda t: datetime.strptime(t[0], '%d/%m/%Y')))
    
    sorted_collection_dict = []

    for x in collection_dict.keys():
        sorted_collection_dict.append({'date':x, 'collecting':collection_dict[x]})
    
    return sorted_collection_dict


@app.route('/bin_details.json')
def bin_details_json():
    return send_from_directory('.','bin_details.json')

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')