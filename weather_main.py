# D Bishop & M Bishop
# 2023 02 20

# Use NWS data to display on InkyWHAT display

# Main Routine --
# This routine gets the weather & displays it using text and icons

import platform  # lets us know if we're on a Raspberry Pi or desktop machine
from PIL import Image, ImageFont, ImageDraw
import math
import numbers
import re
import weather      # Routine to get weather from weather.gov API
import weather_icons # Routine to draw icons

def display_weather(wd):
    # Main routine to create multi-day weather display
    if platform.system() == 'Linux':
        # import inky for Raspberry Pi & Inky display
        from inky import InkyWHAT
        inky_display = InkyWHAT("yellow")
        inky_display.set_border(inky_display.WHITE)
        img = Image.new("P", (inky_display.WIDTH, inky_display.HEIGHT))
        bkgCol = inky_display.WHITE
        prmCol = inky_display.BLACK
        sndCol = inky_display.YELLOW
        colors = [bkgCol, prmCol, sndCol]  # palette indices to make it easier to pass colors to routines

    else:
        # this lets us work on a desktop machine
        img = Image.new("P", (400,300))
        cW = [255, 255, 255]
        cB = [0, 0, 0]
        cY = [255, 255, 0]
        img.putpalette(cW + cB + cY)
        bkgCol = 0
        prmCol = 1
        sndCol = 2
        colors = [bkgCol, prmCol, sndCol]  # palette indices to make it easier to pass colors to routines

    draw = ImageDraw.Draw(img)

    # for debugging
    p = 0  # period

    forecast = re.search(".*[day|night]\/(\w*)", wd['properties']['periods'][p]['icon']).group(1)
    # See: https://api.weather.gov/icons
    
    isDayTime = str(wd['properties']['periods'][p]['isDaytime'])
    
    if forecast == "skc" or forecast == "wind_skc":
        weather_icons.Clear(draw, 200, 150, colors, isDaytime)
    elif forecast == "few" or forecast == "sct" or forecast == "wind_few" or forecast == "wind_sct":
        weather_icons.SemiCloudy(draw, 200, 150, colors, isDayTime)
    elif forecast == "bkn" or forecast == "wind_bkn":
        weather_icons.MostlyCloudy(draw, 200, 150, colors, isDayTime)
    elif forecast == "ovc" or forecast == "wind_ovc":
        weather_icons.Overcast(draw, 200, 150, colors)
    elif forecast =="rain_showers":
        weather_icons.Showers(draw, 200, 150, colors)
    elif forecast =="rain":
        weather_icons.Rain(draw, 200, 150, colors)

    # draw today's temp & forecast
    draw.text((50, 35), wd['properties']['periods'][p]['name'], fill=prmCol)
    draw.text((50, 50), str(wd['properties']['periods'][p]['temperature']), fill=prmCol, align='center')
    draw.text((70, 50), wd['properties']['periods'][p]['shortForecast'], fill=prmCol)
    
    # Draw over code for icon sketching
    draw.rectangle([(0, 0), (400, 300)], colors[0], None, 0)
    weather_icons.Tornado(draw, 200, 150, colors)

    if platform.system() == 'Linux':
        flipped = img.rotate(180)
        inky_display.set_image(flipped)
        inky_display.show()
    else:
        img.convert(mode = "RGB").show()  # preview on PC display

if __name__ == "__main__":
    wd = weather.get_weather()
    display_weather(wd)
    # weather.print_weather(wd, 2)
    