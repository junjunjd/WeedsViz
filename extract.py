import os
from pathlib import Path
import pandas as pd
import re
import json
from geopy.geocoders import GoogleV3
import gmplot
from time import sleep

# prepare site names, coordinates, acreage as a dict

SITES = 'data/DBWSites_Full.csv' 


def get_sites(sitefile: str = SITES):
    """Get the site data in a DataFrame.

    :param sitefile: Path to the file with site IDs, site names, acreage
    :return: A DataFrame with the SITEID, AllNames etc. for each site
    :rtype: pandas.DataFrame
    """
    df = pd.read_csv(sitefile)
    return df.loc[:, ['SITEID', 'AREA',  'ACRES', 'AllNames']]


if __name__ == "__main__":
    geolocator = GoogleV3(api_key="my_API_key")
    sites = get_sites()
    site_dict = {}
    for st in sites.itertuples(index=False):
        print("decoding", st, "....")
        location = geolocator.geocode(st.AllNames + ", California", timeout=10)
        if location is None:
            print ("////////////////////// No Search Result", st.AllNames) 
            site_coordinate = (0, 0)
        else:
            site_coordinate = (location.longitude, location.latitude)    
        
        sleep(1)
        site_dict[st.AllNames] = {"coordinates": site_coordinate, "siteID": st.SITEID, "acreage": st.ACRES} 
    
    with open('site_dict.json', 'w') as fp:
        json.dump(site_dict, fp, indent=1)
   
