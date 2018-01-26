import urllib.request, json
import discord
import math
import time
import re
from collections import OrderedDict

base_url = 'http://tramtracker.com/Controllers/'

def check_tram_number(msg):
    return str.isdigit(msg.content)

def build_dict(seq, key):
     return dict((d[key].split()[0], dict(d, index=index)) for (index, d) in enumerate(seq))

def get_all_stops(stop):
    with open('/tmp/tram.json', 'r') as data:
        routes = json.load(data)

    matched = OrderedDict()
    for route in routes:
        if stop in routes[route]:
            matched[routes[route][stop]['stop_name']] = routes[route][stop]
            matched[routes[route][stop]['stop_name']].update({'route' : route})
         
    if len(matched) == 0: 
        return {'message' : 'No matches found', 'matches' : None}
    
    message = str(len(matched)) + ' stops found \n' 

    for count, match in enumerate(matched): 
        result = str(count) + ' : ' + match + '\n'
        message += result
    
    message += 'Please enter which stop (0 to ' + str(len(matched) - 1) + ') you want' 
    return {'message' : message, 'matches' : matched}

def get_stops(stop, route):
    with open('/tmp/tram.json', 'r') as data:
        stops = json.load(data)

    if route not in stops:
        return 'ERROR_1' 
    elif stop in stops[route]:
        return stops[route][stop]
    else:
        return 'ERROR_2'


def get_next_services(stop, route, all_services, direction = None):
    if stop == 'ERROR_1':
        return 'Error: Could not find route'
    elif stop == 'ERROR_2':
        return 'Error: Could not find stop'
    elif stop is None:
        return 'Error: Something went very very wrong, shout at your nearest Eris dev'
   
    data = dict()    
 
    if direction == 'up' or direction == 'down':
        with urllib.request.urlopen(base_url + 'GetNextPredictionsForStop.ashx?stopNo=' + stop[direction] + '&routeNo=' + ('0' if all_services else route) + '&isLowFloor=false') as url:
            data = json.loads(url.read().decode())
    else:
        with urllib.request.urlopen(base_url + 'GetNextPredictionsForStop.ashx?stopNo=' + stop['up'] + '&routeNo=' + ('0' if all_services else route) + '&isLowFloor=false') as url:
            up_data = json.loads(url.read().decode())
        with urllib.request.urlopen(base_url + 'GetNextPredictionsForStop.ashx?stopNo=' + stop['down'] + '&routeNo=' + ('0' if all_services else route) + '&isLowFloor=false') as url:
            down_data = json.loads(url.read().decode())
        if up_data['hasError'] == False and down_data['hasError'] == False:
            if down_data['responseObject'] and up_data['responseObject']:
                data['responseObject'] = down_data['responseObject'] + up_data['responseObject']
            elif down_data['responseObject']:
                data['responseObject'] = down_data['responseObject']
            elif up_data['responseObject']:
                data['responseObject'] = up_data['responseObject']
            data['hasError'] = False
   
    message = ''
    if(data['hasError'] == False):
        if data['responseObject']:
            for next_services in data['responseObject']:
               result = (int(re.search(r'(\d{10})(\d{3})', next_services['PredictedArrivalDateTime']).group()) / 1000 - time.time()) / 60
               service = str(math.floor(result)) + ' minutes: Route ' + str(next_services['RouteNo']) + ' to ' + next_services['Destination'] + ' (tram #'  + str(next_services['VehicleNo']) + ')'
               if next_services['AirConditioned'] == True:
                   service += ' :snowflake:'
               message += service + '\n'
            return message
        else:
            return 'Error: Could not find upcoming services for stop id ' + stop['stop_number']
    else:
        return 'Error: Could not load JSON upcoming services data' 
