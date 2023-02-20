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

    draw = ImageDraw.Draw(img)

    #myCircle((200, 150), 96, None, prmCol, 1)

    # for debugging
    p = 0  # period

    forecast = re.search(".*[day|night]\/(\w*)", wd['properties']['periods'][p]['icon']).group(1)
    # See: https://api.weather.gov/icons
    if forecast == "skc" or forecast == "few":
        weather_icons.Sunny(200, 150)
    elif forecast == "sct":
        weather_icons.PartlySunny(200, 150)
    elif forecast == "bkn":
        weather_icons.PartlyCloudy(200, 150)
    elif forecast == "ovc":
        weather_icons.Cloudy(200, 150)
    elif forecast =="rain_showers":
        weather_icons.Raining(200, 150)

    # from font_fredoka_one import FredokaOne
    # font = ImageFont.truetype(FredokaOne, 36)

    # draw today's temp & forecast
    #draw.text((195, 100), str(wd['properties']['periods'][0]['temperature']), fill=prmCol, align='center', font=font)
    draw.text((50, 35), wd['properties']['periods'][p]['name'], fill=prmCol)
    draw.text((50, 50), str(wd['properties']['periods'][p]['temperature']), fill=prmCol, align='center')  # without font choice
    draw.text((70, 50), wd['properties']['periods'][p]['shortForecast'], fill=prmCol)

    if platform.system() == 'Linux':
        flipped = img.rotate(180)
        inky_display.set_image(flipped)
        inky_display.show()
    else:
        # try scaling
        img_quarter = img.resize((200,150))
        for i in range(0, 2):
            for j in range(0, 2):
                img.paste(img_quarter, (200*i,150*j))
        
        img.convert("RGB").show()  # preview on PC display
    img.convert("RGB").show()  # preview on PC display


if __name__ == "__main__":
	wd = weather.get_weather()
	display_weather(wd)