# D Bishop & M Bishop
# 2023 01 18

# Read data from the NWS & parse
 
import urllib.request 
import json

<<<<<<< HEAD
def get_weather():
    # read weather from URL to get string & parse JSON to a python dictionary
    response = urllib.request.urlopen('https://api.weather.gov/gridpoints/PBZ/70,69/forecast')  # Sewickley, PA
    weather_dict = json.loads(response.read())
    return weather_dict

def print_weather(weather_dict):
    for i in range(4):
        print(weather_dict['properties']['periods'][i]['name'])
        print('Temperature ' + str(weather_dict['properties']['periods'][i]['temperature']) + "˚F")
        print('Wind ' + weather_dict['properties']['periods'][i]['windSpeed'])
        print(weather_dict['properties']['periods'][i]['shortForecast'])
        print("")

#wd = get_weather()
#print_weather(wd)
=======
for i in range(4):
	print(weather_dict['properties']['periods'][i]['name'])
	print('Temperature ' + str(weather_dict['properties']['periods'][i]['temperature']) + "˚F")
	print('Wind ' + weather_dict['properties']['periods'][i]['windSpeed'] + " from the " + weather_dict['properties']['periods'][i]['windDirection'])
	print(weather_dict['properties']['periods'][i]['shortForecast'])
	print("")
>>>>>>> cfdbe457229705c40478a9cea2143bbe8ab979c4
