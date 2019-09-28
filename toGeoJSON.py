import datetime
import os
from pathlib import Path
import pandas as pd
import re
import json
from geopy.geocoders import GoogleV3
import gmplot
from time import sleep

SITES = 'data/DBW_data.csv'
SITE_DICT = 'site_dict.json'

site_dict = json.load(open(SITE_DICT))



geojson = {
    "type": "FeatureCollection",
    "features": [
    {
        "type": "Feature",
        "geometry" : {
            "type": "Point",
            "coordinates": [d, d["lat"]],
            },
        "properties" : d,
     } for d in data]
}


output = open(out_file, 'w')
json.dump(geojson, output)