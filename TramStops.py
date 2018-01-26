import urllib.request, json

base_url = 'http://tramtracker.com/Controllers/'

key = {}

with urllib.request.urlopen(base_url + '/GetAllRoutes.ashx') as url:
    routes = json.loads(url.read().decode())

for route in routes['ResponseObject']:
    key[route['RouteNo']] = {}

    with urllib.request.urlopen(base_url + '/GetStopsByRouteAndDirection.ashx?r=' + str(route['RouteNo']) + '&u=true') as url:
        up_stops = json.loads(url.read().decode())['ResponseObject']
    
    with urllib.request.urlopen(base_url + '/GetStopsByRouteAndDirection.ashx?r=' + str(route['RouteNo']) + '&u=false') as url:
        down_stops = json.loads(url.read().decode())['ResponseObject']

    for stop in up_stops:
        key[route['RouteNo']][stop['StopName'].split()[0]] = {'stop_name' : stop['Description'], 'up' : str(stop['StopNo'])}

    for stop in down_stops:
        if stop['StopName'].split()[0] in key[route['RouteNo']]:
            key[route['RouteNo']][stop['StopName'].split()[0]]['down'] = str(stop['StopNo'])
        else:
            key[route['RouteNo']][stop['StopName'].split()[0]] = {'stop_name' : stop['Description'], 'down' : str(stop['StopNo'])}
        
        

with open('/tmp/tram.json', 'w') as data:
    data.truncate(0)
    json.dump(key, data)
