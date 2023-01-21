# D Bishop & M Bishop
# 2023 01 18

# Read data from the NWS & parse
 
import urllib.request 
import json
 
# read weather from URL to get string & parse JSON to a python dictionary
response = urllib.request.urlopen('https://api.weather.gov/gridpoints/PBZ/70,69/forecast')  # Sewickley, PA
weather_dict = json.loads(response.read())

for i in range(4):
	print(weather_dict['properties']['periods'][i]['name'])
	print('Temperature ' + str(weather_dict['properties']['periods'][i]['temperature']) + "˚F")
	print('Wind ' + weather_dict['properties']['periods'][i]['windSpeed'] + " from the " + weather_dict['properties']['periods'][i]['windDirection'])
	print(weather_dict['properties']['periods'][i]['shortForecast'])
	print("")