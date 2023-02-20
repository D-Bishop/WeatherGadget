# D Bishop & M Bishop
# 2023 01 18

# Use NWS data to display on InkyWHAT display

# IDIOM
# try:
#     import json
# except ImportError:
#     import simplejson as json

import platform  # lets us know if we're on a Raspberry Pi or desktop machine -- for debugging
from PIL import Image, ImageFont, ImageDraw
import math
import numbers
import re
import weather  # Bishop's routine to get weather from weather.gov API


def _compute_regular_polygon_vertices(bounding_circle, n_sides, rotation):
    # 1. Error Handling
    # 1.1 Check `n_sides` has an appropriate value
    if not isinstance(n_sides, int):
        raise TypeError("n_sides should be an int")
    if n_sides < 3:
        raise ValueError("n_sides should be an int > 2")

    # 1.2 Check `bounding_circle` has an appropriate value
    if not isinstance(bounding_circle, (list, tuple)):
        raise TypeError("bounding_circle should be a tuple")

    if len(bounding_circle) == 3:
        *centroid, polygon_radius = bounding_circle
    elif len(bounding_circle) == 2:
        centroid, polygon_radius = bounding_circle
    else:
        raise ValueError(
            "bounding_circle should contain 2D coordinates "
            "and a radius (e.g. (x, y, r) or ((x, y), r) )"
        )

    if not all(isinstance(i, (int, float)) for i in (*centroid, polygon_radius)):
        raise ValueError("bounding_circle should only contain numeric data")

    if not len(centroid) == 2:
        raise ValueError(
            "bounding_circle centre should contain 2D coordinates (e.g. (x, y))"
        )

    if polygon_radius <= 0:
        raise ValueError("bounding_circle radius should be > 0")

    # 1.3 Check `rotation` has an appropriate value
    if not isinstance(rotation, (int, float)):
        raise ValueError("rotation should be an int or float")

    # 2. Define Helper Functions
    def _apply_rotation(point, degrees, centroid):
        return (
            round(
                point[0] * math.cos(math.radians(360 - degrees))
                - point[1] * math.sin(math.radians(360 - degrees))
                + centroid[0],
                2,
            ),
            round(
                point[1] * math.cos(math.radians(360 - degrees))
                + point[0] * math.sin(math.radians(360 - degrees))
                + centroid[1],
                2,
            ),
        )

    def _compute_polygon_vertex(centroid, polygon_radius, angle):
        start_point = [polygon_radius, 0]
        return _apply_rotation(start_point, angle, centroid)

    def _get_angles(n_sides, rotation):
        angles = []
        degrees = 360 / n_sides
        # Start with the bottom left polygon vertex
        current_angle = (270 - 0.5 * degrees) + rotation
        for _ in range(0, n_sides):
            angles.append(current_angle)
            current_angle += degrees
            if current_angle > 360:
                current_angle -= 360
        return angles

    # 3. Variable Declarations
    angles = _get_angles(n_sides, rotation)

    # 4. Compute Vertices
    return [
        _compute_polygon_vertex(centroid, polygon_radius, angle) for angle in angles
    ]

def myCircle(centerPos, radius, fillColour, outlineColour, outlineWidth):
    centerX = centerPos[0]
    centerY = centerPos[1]

    draw.ellipse([(centerX-radius,centerY-radius),(centerX+radius,centerY+radius)],
    fill=fillColour, outline=outlineColour, width=outlineWidth)


def myArc(centerPos, radius, start, end, fillColour, outlineWidth):
    centerX = centerPos[0]
    centerY = centerPos[1]

    draw.arc([(centerX-radius,centerY-radius),(centerX+radius,centerY+radius)], start,
    end, fill=fillColour, width=outlineWidth)

def star(bounding_circle, fillColour, lineLength, outlineWidth, n_lines, rotation):
    myOutVert = _compute_regular_polygon_vertices(bounding_circle, n_lines, rotation)
    myInVert = _compute_regular_polygon_vertices((bounding_circle[0],bounding_circle[1],
    bounding_circle[2] - lineLength), n_lines, rotation)

    for k in range(n_lines):
    # TODO Figure out if last two lines are necessesary
        draw.line((myOutVert[k], myInVert[k]), fillColour, outlineWidth)
        
        myCircle(myOutVert[k] , 2, fillColour, None, 0)
        myCircle(myInVert[k], 2, fillColour, None, 0)

def myStars(xPos, yPos):
    draw.line([(xPos+24, yPos-8), (236,142)], fill=prmCol, width=5)
    draw.line([(xPos+30, yPos-14), (230,148)], fill=prmCol, width=5)

    myCircle((xPos+24, yPos-8), 2, prmCol, None, 0)
    myCircle((xPos+36, yPos-8), 2, prmCol, None, 0)

    myCircle((xPos+30, yPos-14), 2, prmCol, None, 0)
    myCircle((xPos+30, yPos-2), 2, prmCol, None, 0)

    draw.line([(xPos-2, yPos-26), (222,124)], fill=prmCol, width=5)
    draw.line([(xPos+10, yPos-38), (210,136)], fill=prmCol, width=5)

    myCircle((xPos-2, yPos-26), 2, prmCol, None, 0)
    myCircle((xPos+22, yPos-26), 2, prmCol, None, 0)

    myCircle((xPos+10, yPos-38), 2, prmCol, None, 0)
    myCircle((xPos+10, yPos-14), 2, prmCol, None, 0)
    
def myMoon(xPos, yPos):
    myCircle((xPos, yPos), 48, sndCol, prmCol, 5)
    myCircle((xPos+18, yPos-16), 40, bkgCol, None, 0)

    myArc((xPos+18, yPos-16), 40, 47, 234, prmCol, 5)

def mySunny(xPos, yPos):
    myCircle((xPos, yPos), 32, sndCol, prmCol, 5)
    star((xPos, yPos, 64), prmCol, 22, 7, 8, 22.5)
    
def myCloudy(xPos, yPos):
    myCircle((xPos+20, yPos), 42, bkgCol, None, 0)
    myCircle((xPos-32, yPos+9), 33, bkgCol, None, 0)
    
    myArc((xPos+20, yPos), 42, 203, 90, prmCol, 5)
    myArc((xPos-32, yPos+9), 33, 90, 346, prmCol, 5)
    draw.line([(xPos+20, yPos+41), (xPos-32, yPos+41)], fill=prmCol, width=5)
    
    myCircle((xPos-2, yPos+1), 2, prmCol, None, 0)
    
def myCloudWGap(xPos, yPos):
    myArc((xPos+20, yPos), 42, 203, 90-23, prmCol, 5)
    myArc((xPos-32, yPos+9), 33, 90+6, 346, prmCol, 5)
    
    myCircle((xPos-2, yPos+1), 2, prmCol, None, 0)
    
    myCircle((xPos-35, yPos+40), 2, prmCol, None, 0)

def mySmallSun(xPos, yPos):
    myCircle((xPos-20, yPos-28), 21, sndCol, prmCol, 5)
    star((xPos-20, yPos-28, 43), prmCol, 14, 7, 8, 22.5)
    
def mySmallCloud(xPos, yPos):
    myCircle((xPos+31, yPos+29), 28, bkgCol, None, 0)
    myCircle((xPos-4, yPos+35), 22, bkgCol, None, 0)
    draw.rectangle([(xPos-10, yPos+25), (xPos+10, yPos+70)], bkgCol, None, 0)

    myArc((xPos+31, yPos+29), 28, xPos, 90, prmCol, 5)
    myArc((xPos-4, yPos+35), 22, 90, 346, prmCol, 5)
    draw.line([(xPos+31, yPos+56), (xPos-4, yPos+56)], fill=prmCol, width=5)
    
def mySmallMoon(xPos, yPos):
    myCircle((xPos-3, yPos-34), 32, sndCol, prmCol, 5)
    myCircle((xPos+9, yPos-45), 27, bkgCol, None, 0)

    myArc((xPos+9, yPos-45), 27, 46, 230, prmCol, 5)

def myPartlySunny(xPos, yPos):
    mySunny(xPos, yPos)
    mySmallCloud(xPos, yPos)
    
def myPartlyCloudy(xPos, yPos):
    mySmallSun(xPos, yPos)
    myCloudy(xPos, yPos)

def myClearNight(xPos, yPos):
    myMoon(xPos, yPos)
    myStars(xPos, yPos)

def myMostlyClearNight(xPos, yPos):
    myMoon(xPos, yPos)
    mySmallCloud(xPos, yPos)
    
def myMostlyCloudyNight(xPos, yPos):
    mySmallMoon(xPos, yPos)
    myCloudy(xPos, yPos)
    
def myRaining(xPos, yPos):
    myCloudWGap(xPos, yPos)
    
    draw.line([(xPos-16, yPos+30), (xPos-32, yPos+58)], fill=prmCol, width=5)	#line1
    draw.line([(xPos-2, yPos+30), (xPos-22, yPos+65)], fill=prmCol, width=5)	#line2
    draw.line([(xPos+12, yPos+30), (xPos-4, yPos+58)], fill=prmCol, width=5)	#line3
    draw.line([(xPos+26, yPos+30), (xPos-2, yPos+79)], fill=prmCol, width=5)	#line4
    
    myCircle((xPos-16, yPos+30), 2, prmCol, None, 0), myCircle((xPos-32, yPos+58), 2, prmCol, None, 0)
    myCircle((xPos-2, yPos+30), 2, prmCol, None, 0), myCircle((xPos-22, yPos+65), 2, prmCol, None, 0)
    myCircle((xPos+12, yPos+30), 2, prmCol, None, 0), myCircle((xPos-4, yPos+58), 2, prmCol, None, 0)
    myCircle((xPos+26, yPos+30), 2, prmCol, None, 0), myCircle((xPos-2, yPos+79), 2, prmCol, None, 0)
    
def myDrizzle(xPos, yPos):
    myCloudWGap(xPos, yPos)
    # Rule is x-4 for y+7 to move down
    
    draw.line([(xPos-20, yPos+37), (xPos-28, yPos+51)], fill=prmCol, width=5)	#line1
    draw.line([(xPos+2, yPos+23), (xPos-6, yPos+37)], fill=prmCol, width=5)		#line2
    draw.line([(xPos-18, yPos+58), (xPos-26, yPos+72)], fill=prmCol, width=5)	#line2b
    draw.line([(xPos+4, yPos+44), (xPos-4, yPos+58)], fill=prmCol, width=5)		#line3
    draw.line([(xPos+26, yPos+30), (xPos+18, yPos+44)], fill=prmCol, width=5)	#line4
    draw.line([(xPos+6, yPos+65), (xPos-2, yPos+79)], fill=prmCol, width=5)		#line4b
    
    myCircle((xPos-20, yPos+37), 2, prmCol, None, 0), myCircle((xPos-28, yPos+51), 2, prmCol, None, 0)
    myCircle((xPos+2, yPos+23), 2, prmCol, None, 0), myCircle((xPos-6, yPos+37), 2, prmCol, None, 0)
    myCircle((xPos-18, yPos+58), 2, prmCol, None, 0), myCircle((xPos-26, yPos+72), 2, prmCol, None, 0)
    myCircle((xPos+4, yPos+44), 2, prmCol, None, 0), myCircle((xPos-4, yPos+58), 2, prmCol, None, 0)
    myCircle((xPos+26, yPos+30), 2, prmCol, None, 0), myCircle((xPos+18, yPos+44), 2, prmCol, None, 0)
    myCircle((xPos+6, yPos+65), 2, prmCol, None, 0), myCircle((xPos-2, yPos+79), 2, prmCol, None, 0)
    
    
#------------------------------------------------------------

if __name__ == "__main__":

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

    # myCircle((200, 150), 96, None, prmCol, 1)
    myPartlyCloudy(200, 150)
    
    if platform.system() == 'Linux':
        flipped = img.rotate(180)
        inky_display.set_image(flipped)
        inky_display.show()
    else:
        # try scaling
        img_crop = img.crop((100, 50, 300, 250))
        img_quarter = img_crop.resize((75, 75))
        
        draw.rectangle([(0, 0), (400, 300)], bkgCol, None, 0)
        myRaining(200, 150)
        img_crop2 = img.crop((100, 50, 300, 250))
        img_quarter2 = img_crop2.resize((75, 75))
        
        draw.rectangle([(0, 0), (400, 300)], bkgCol, None, 0)
        myPartlySunny(200, 150)
        img_crop3 = img.crop((100, 50, 300, 250))
        img_quarter3 = img_crop3.resize((75, 75))
        
        draw.rectangle([(0, 0), (400, 300)], bkgCol, None, 0)
        mySunny(200, 150)
        img_crop4 = img.crop((100, 50, 300, 250))
        img_quarter4 = img_crop4.resize((75, 75))
        
        draw.rectangle([(0, 0), (400, 300)], bkgCol, None, 0)
        myCloudy(162, 150)
        img.paste(img_quarter, (300, 0))
        img.paste(img_quarter2, (300, 75))
        img.paste(img_quarter3, (300, 75+75))
        img.paste(img_quarter4, (300, 75+75+75))
        
        img.convert("RGB").show()  # preview on PC display