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


def get_sites(sitefile: str = SITES):
    """Get the site data in a DataFrame.

    :param sitefile: Path to the file with site IDs and acreage
    :return: A DataFrame with the SITEID and Site_Name for each site
    :rtype: pandas.DataFrame
    """
    df = pd.read_csv(sitefile)
    return df.loc[:, ['SiteID', 'Site_Name']]


if __name__ == "__main__":
    geolocator = GoogleV3(api_key="AIzaSyCsbn3cVnvFfU15T3ugB_a0d3R7C2tuD_g")
    sites = get_sites()
    site_list = sites['Site_Name'].unique()
    site_dict = {}
    for st in site_list:
        if isinstance(st, float):
            st = "nan"
            site_coordinate = (0, 0)
        else:
            location = geolocator.geocode(st + ", California", timeout=10)
            if location is None:
                print ("////////////////////// No Search Result", st) 
                site_coordinate = (0, 0)
            else:
                site_coordinate = (location.latitude, location.longitude)    
        
        sleep(1)
        site_dict[st] = site_coordinate
    
    with open('site_dict.json', 'w') as fp:
        json.dump(site_dict, fp, indent=1)
   
