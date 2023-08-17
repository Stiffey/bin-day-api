from datetime import datetime
from flask import Flask, send_from_directory, request
# from pathlib import Path
import json
import urllib.request, json
import os
import time

from flask_cors import CORS

app = Flask(__name__)
# app.debug = True
CORS(app)

@app.route('/')
def next_collection():

    URL_root = request.url_root
    print("URL_root")

    # Read JSON bin details
    with urllib.request.urlopen(URL_root + '/bin_details.json') as f:
        print("with")
        collection_dict = json.load(f)
        print("dictionary loaded")

        # Get current date
        current_date = datetime.now()
        print("current date")

        # Look through dates and find closest collection
        for dates in collection_dict.keys():
            print("loop started")
            date = datetime.strptime(dates, '%d/%m/%Y')
            print("dates")
            days_to_collection = date - current_date
            print("days to collection")
            # print(days_to_collection)
            if days_to_collection.days < 6:
                print("if less than 6")
                next_bin_collection = collection_dict[dates]
                next_bin_collection_date = date
                next_bin_collection_date_formated = next_bin_collection_date.strftime("%A %d %B")

                # Define the next collection
                if 'Refuse Collection Service' in next_bin_collection:
                    next_bin_collection = "black"
                    # img = ['static/img/Refuse Collection Service.png']
                elif 'Recycling Collection Service' in next_bin_collection and 'Garden Waste Collection Service' not in next_bin_collection:
                    next_bin_collection = "blue"
                    # img = ['static/img/Recycling Collection Service.png']
                elif 'Garden Waste Collection Service' in next_bin_collection and 'Recycling Collection Service' not in next_bin_collection:
                    next_bin_collection = "brown"
                    # img = ['static/img/Garden Waste Collection Service.png']
                elif 'Recycling Collection Service' in next_bin_collection and 'Garden Waste Collection Service' in next_bin_collection:
                    next_bin_collection = "blue and brown"
                    # img = ['static/img/Recycling Collection Service.png', 'static/img/Garden Waste Collection Service.png']
                else:
                    next_bin_collection = "dunno"

        path = 'app/bin_details.json'
        ti_m = os.path.getmtime(path)
        m_ti = time.ctime(ti_m)
        print("Time thing")

        bin_collection_dict = {
            'date' : next_bin_collection_date_formated,
            'collecting' : next_bin_collection,
            'last_updated' : m_ti
        }

        return bin_collection_dict
    

@app.route('/bin_details.json')
def bin_details_json():
    return send_from_directory('.','bin_details.json')



@app.route('/about')
def about():
    return "This is an about page"

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')