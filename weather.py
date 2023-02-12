# D Bishop & M Bishop
# 2023 01 18

# Read data from the NWS & parse
#
# • Returns weather as the JSON structure from the NWS
# • Documentation here: https://www.weather.gov/documentation/services-web-api
# • Hard-coded to Sewickley for the time being

 
import urllib.request 
import json

def get_weather():
    # read weather from URL to get string & parse JSON to a python dictionary
    response = urllib.request.urlopen('https://api.weather.gov/gridpoints/PBZ/70,69/forecast')  # Sewickley, PA
    weather_dict = json.loads(response.read())
    return weather_dict

def print_weather(weather_dict, days):
    for i in range(0, int(days * 2)):
        print(str(i) + ' ' + str(weather_dict['properties']['periods'][i]['number']))
        print(weather_dict['properties']['periods'][i]['name'])
        print('Temperature ' + str(weather_dict['properties']['periods'][i]['temperature']) + "˚F")
        print('Wind ' + weather_dict['properties']['periods'][i]['windSpeed'])
        print(weather_dict['properties']['periods'][i]['shortForecast'])
        print(weather_dict['properties']['periods'][i]['icon'])
        print('P.O.P. ' + str(weather_dict['properties']['periods'][i]['probabilityOfPrecipitation']['value']))
        print("")


if __name__ == "__main__":    
    wd = get_weather()
    print_weather(wd, 1)