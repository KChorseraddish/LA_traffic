import requests
from datetime import datetime
import csv

"""Base Url to start the search query"""

base_url='https://api.tomtom.com/traffic/services/4/flowSegmentData/relative-delay/'

"""Dictionary with street name and latitude and longitude coordinates. Coordinates needed
for building the complete search url."""

street_long_and_lat_dict = {'Vermont':'34.011584,-118.291582',
                            'MLK':'34.011130,-118.285862',
                            'Exposition':'34.018360,-118.287385',
                            }
"""API_key is currently set to mine. Replace the key by registering for your own TomTom API 
Key here: https://developer.tomtom.com/user/register"""

API_key = 'UesdCK9LKchNS0XXgcB63PWbaK7aFh0k'

"""Function to build the complete search URL"""
def url_build(street_name, zoom_level):
    if street_name in street_long_and_lat_dict:
        return base_url + zoom_level + '/json' + '?key=' + API_key + '&point=' + street_long_and_lat_dict[street_name] + '&unit=mph'
    else:
        print('Street name not found. Please make sure your street name is spelled correctly.')

"""Function to convert the requested JSON into a list of current and max speeds and times."""
def json_to_list(json_data):
    json_speed_data = json_data['flowSegmentData']
    speed_list = []
    speed_list.append(json_speed_data['currentSpeed'])
    speed_list.append(json_speed_data['freeFlowSpeed'])
    speed_list.append(json_speed_data['currentTravelTime'])
    speed_list.append(json_speed_data['freeFlowTravelTime'])
    return speed_list

"""Function to compute a travel time ratio based on current time to travel over optimal travel time. Returns
   a string describing the traffic severity level."""
def traffic_severity_calculator(speed_list):
    travel_ratio = speed_list[2]/speed_list[3]
    if travel_ratio >= 0.9:
        return 'low to mild traffic'
    elif travel_ratio >= 0.7 and travel_ratio < 0.9:
        return 'moderate traffic'
    else:
        return 'severe traffic'

"""Function to write a CSV file that has the speeds and travel estimates for a given time on a
particular street."""
def csv_write(speed_list,street_name):
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    travel_rating = traffic_severity_calculator(speed_list)
    header_list = ['Current Speed(mph)','Max Speed(mph)','Current Travel Time(seconds)',
                'Quickest Travel Time(seconds)','Street Name','Traffic Severity Score''Date & Time']
    speed_list.append(street_name)
    speed_list.append(travel_rating)
    speed_list.append(dt_string)
    with open('rams_road_traffic.csv','w',newline='') as file:
        writer = csv.writer(file)
        writer.writerow(header_list)
        writer.writerow(speed_list)

"""Main function to drive the program."""
def main_driver(street_name):
    url = url_build(street_name,'15')
    resp = requests.get(url=url)
    data = resp.json()
    speed_list = json_to_list(data)
    csv_write(speed_list,street_name)

"""Insert street name to be tested as a parameter below"""
main_driver('Vermont')