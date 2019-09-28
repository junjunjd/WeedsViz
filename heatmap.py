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
MAP = 'map.html'
SITE_DICT = 'site_dict.json'

gmap = gmplot.GoogleMapPlotter.from_geocode("Dehradun, India")

gmap4.draw(MAP)

