import datetime
import os
import string
from pathlib import Path
import pandas as pd
import re
import json
from geopy.geocoders import GoogleV3
import gmplot
from time import sleep
import matplotlib

SITES = 'data/DBW_data.csv'
SITE_DICT = 'site_dict_new.json'

site_dict = json.load(open(SITE_DICT))

# new_site_dict = {}

# for st, info in site_dict.items():

#     t = re.sub("\D", "", info['siteID'])
#     new_site_dict[t] = {"coordinates": info['coordinates'], "site_Name": st}

# with open('site_dict_new.json', 'w') as fp:
#     json.dump(site_dict, fp, indent=1)

dateparse = lambda x: pd.datetime.strptime(x, '%m/%d/%y')

def get_sites(sitefile: str = SITES):
    """Get the site data in a DataFrame.

    :param sitefile: Path to the file with site IDs and acreage
    :return: A DataFrame with the SITEID and Site_Name for each site
    :rtype: pandas.DataFrame
    """
    df = pd.read_csv(sitefile, parse_dates=['Date'], date_parser=dateparse)
    return df.loc[:, ['SiteID', 'Site_Name', "Site_Acres", 'Date', "gal_D", 'gal_Glyphosate', "acres_D", "acres_Glyphosate"]]


sites = get_sites()
dt = sites.groupby('SiteID').max()

year = []

for d in sites.itertuples(index=False):
    year = year + [d.Date.year]
    

sites['Year'] = year

treat_count_by_year = sites.groupby('Year')['SiteID'].value_counts()

Glyphosate_by_site_year = sites.groupby(['Year','SiteID'])['gal_Glyphosate'].sum()
D24_by_site_year = sites.groupby(['Year','SiteID'])['gal_D'].sum()
Glyphosate_acre_by_site_year = sites.groupby(['Year','SiteID'])['acres_Glyphosate'].sum()
D24_acre_by_site_year = sites.groupby(['Year','SiteID'])['acres_D'].sum()

print("count by year /////////////////////////////", list(treat_count_by_year))

geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "description": "<!DOCTYPE html><html><head><style>table {font-family: arial, sans-serif;border-collapse: collapse;width: 100%;}td, th {border: 1px solid #dddddd;text-align: left;padding: 8px;}tr:nth-child(even) {background-color: #dddddd;}</style></head><body><h2>Site " + str(m[1]) + ": " + site_dict.get(str(m[1]), "Site Name Not Found")['site_Name'] + "</h2><h2>Site Acreage: " + str(round(dt.get_value(m[1],"Site_Acres"))) + "</h2><table><tr><th>Herbicide</th><th>Gallons</th><th>Acres Treated</th></tr><tr><td>Glyphosate</td><td>" + str(round(Glyphosate_by_site_year[m[0],m[1]])) + "</td><td>" + str(round(Glyphosate_acre_by_site_year[m[0],m[1]])) + "</td></tr><tr><td>2,4-D</td><td>" + str(round(D24_by_site_year[m[0],m[1]])) + "</td><td>" + str(round(D24_acre_by_site_year[m[0],m[1]])) + "</td></tr></table></body></html>", 
                
                "siteID": m[1],
                "site_Name": site_dict.get(str(m[1]), "Site Name Not Found")['site_Name'],
                "Acreage": dt.get_value(m[1],"Site_Acres"),
                "Treatment": n,
                "Year": m[0],
            },
            "geometry": {
                "type": "Point",
                "coordinates": [site_dict.get(str(m[1]), "Site Name Not Found")['coordinates'][0],site_dict.get(str(m[1]), "Site Name Not Found")['coordinates'][1]],
            },
        } for m, n in treat_count_by_year.items()]
}


output = open('treat_count_by_year1.json', 'w')
json.dump(geojson, output, indent=1) 
