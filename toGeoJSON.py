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


def get_sites(sitefile: str = SITES):
    """Get the site data in a DataFrame.

    :param sitefile: Path to the file with site IDs and acreage
    :return: A DataFrame with the SITEID and Site_Name for each site
    :rtype: pandas.DataFrame
    """
    df = pd.read_csv(sitefile)
    return df.loc[:, ['SiteID', 'Site_Name', 'Date']]


sites = get_sites()

site_count = sites['Site_Name'].value_counts()

print (site_count)
""" 

geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "Treatment": n,
            },
            "geometry": {
                "type": "Point",
                "coordinates": [site_dict.get(m, "Site Name Not Found")[1],site_dict.get(m, "Site Name Not Found")[0]],
            },
        } for m, n in site_count.items()]
}


output = open('treat_count_all.json', 'w')
json.dump(geojson, output, indent=1) """
