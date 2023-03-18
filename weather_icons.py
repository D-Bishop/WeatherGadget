# D Bishop & M Bishop
# 2023 01 18

# definitions for weather icons

import platform  # lets us know if we're on a Raspberry Pi or desktop machine -- for debugging
from PIL import Image, ImageFont, ImageDraw
import math
import numbers

class WeatherImage():
    def __init__(self):
        # this needs the if statements to choose between Pi & desktop machines
        # that is: if platform.system() == 'Linux': etc., etc.
        self.img = Image.new("P", (400,300))
        cW = [255, 255, 255]
        cB = [0, 0, 0]
        cY = [255, 255, 0]
        self.img.putpalette(cW + cB + cY)
        self.draw = ImageDraw.Draw(self.img)
        self.BLACK = 0
        bkgCol = 0
        prmCol = 1
        sndCol = 2
        
    # TODO Was this for the demo below?
    def cloud(self, xPos, yPos):
        self.draw.line([(xPos+6, yPos+65), (xPos-2, yPos+79)], fill=self.BLACK, width=5)
    def show(self):
        self.img.convert(mode = "RGB").show()

# Example code for ObjectOriented Demo for Marin
# wi = WeatherImage()
# wi.cloud(200, 150)
# wi.show()

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

def Circle(draw, centerPos, radius, fillColour, outlineColour, outlineWidth):
    centerX = centerPos[0]
    centerY = centerPos[1]

    draw.ellipse([(centerX-radius,centerY-radius),(centerX+radius,centerY+radius)],
    fill=fillColour, outline=outlineColour, width=outlineWidth)


def Arc(draw, centerPos, radius, start, end, fillColour, outlineWidth):
    centerX = centerPos[0]
    centerY = centerPos[1]

    draw.arc([(centerX-radius,centerY-radius),(centerX+radius,centerY+radius)], start,
    end, fill=fillColour, width=outlineWidth)

def star(draw, bounding_circle, fillColour, lineLength, outlineWidth, n_lines, rotation):
    myOutVert = _compute_regular_polygon_vertices(bounding_circle, n_lines, rotation)
    myInVert = _compute_regular_polygon_vertices((bounding_circle[0],bounding_circle[1],
    bounding_circle[2] - lineLength), n_lines, rotation)

    for k in range(n_lines):
    # TODO Figure out if last two lines are necessesary
        draw.line((myOutVert[k], myInVert[k]), fillColour, outlineWidth)
        
        Circle(draw, myOutVert[k] , 2, fillColour, None, 0)
        Circle(draw, myInVert[k], 2, fillColour, None, 0)

def Stars(draw, xPos, yPos, colors):
    draw.line([(xPos+24, yPos-8), (236,142)], fill=colors[1], width=5)
    draw.line([(xPos+30, yPos-14), (230,148)], fill=colors[1], width=5)

    Circle(draw, (xPos+24, yPos-8), 2, colors[1], None, 0)
    Circle(draw, (xPos+36, yPos-8), 2, colors[1], None, 0)

    Circle(draw, (xPos+30, yPos-14), 2, colors[1], None, 0)
    Circle(draw, (xPos+30, yPos-2), 2, colors[1], None, 0)

    draw.line([(xPos-2, yPos-26), (222,124)], fill=colors[1], width=5)
    draw.line([(xPos+10, yPos-38), (210,136)], fill=colors[1], width=5)

    Circle(draw, (xPos-2, yPos-26), 2, colors[1], None, 0)
    Circle(draw, (xPos+22, yPos-26), 2, colors[1], None, 0)

    Circle(draw, (xPos+10, yPos-38), 2, colors[1], None, 0)
    Circle(draw, (xPos+10, yPos-14), 2, colors[1], None, 0)
    
def Moon(draw, xPos, yPos, colors):
    Circle(draw, (xPos, yPos), 48, colors[2], colors[1], 5)
    Circle(draw, (xPos+18, yPos-16), 40, colors[0], None, 0)

    Arc(draw, (xPos+18, yPos-16), 40, 47, 234, colors[1], 5)

def Sun(draw, xPos, yPos, colors):
    Circle(draw, (xPos, yPos), 32, colors[2], colors[1], 5)
    star(draw, (xPos, yPos, 64), colors[1], 22, 7, 8, 22.5)
    
def CloudWGap(draw, xPos, yPos, colors):
    Arc(draw, (xPos+20, yPos), 42, 203, 90-23, colors[1], 5)
    Arc(draw, (xPos-32, yPos+9), 33, 90+6, 346, colors[1], 5)
    
    Circle(draw, (xPos-2, yPos+1), 2, colors[1], None, 0)
    
    Circle(draw, (xPos-35, yPos+40), 2, colors[1], None, 0)

def SmallSun(draw, xPos, yPos, colors):
    Circle(draw, (xPos-20, yPos-28), 21, colors[2], colors[1], 5)
    star(draw, (xPos-20, yPos-28, 43), colors[1], 14, 7, 8, 22.5)
    
def SmallCloud(draw, xPos, yPos, colors):
    Circle(draw, (xPos+31, yPos+29), 28, colors[0], None, 0)
    Circle(draw, (xPos-4, yPos+35), 22, colors[0], None, 0)
    draw.rectangle([(xPos-10, yPos+25), (xPos+10, yPos+70)], colors[0], None, 0)

    Arc(draw, (xPos+31, yPos+29), 28, xPos, 90, colors[0], 5)
    Arc(draw, (xPos-4, yPos+35), 22, 90, 346, colors[0], 5)
    draw.line([(xPos+31, yPos+56), (xPos-4, yPos+56)], fill=colors[1], width=5)
    
def SmallMoon(draw, xPos, yPos, colors):
    Circle(draw, (xPos-3, yPos-34), 32, colors[2], colors[1], 5)
    Circle(draw, (xPos+9, yPos-45), 27, colors[0], None, 0)

    Arc(draw, (xPos+9, yPos-45), 27, 46, 230, colors[1], 5)


def Overcast(draw, xPos, yPos, colors):
    Circle(draw, (xPos+20, yPos), 42, colors[0], None, 0)
    Circle(draw, (xPos-32, yPos+9), 33, colors[0], None, 0)
    
    Arc(draw, (xPos+20, yPos), 42, 203, 90, colors[1], 5)
    Arc(draw, (xPos-32, yPos+9), 33, 90, 346, colors[1], 5)
    draw.line([(xPos+20, yPos+41), (xPos-32, yPos+41)], fill=colors[1], width=5)
    
    Circle(draw, (xPos-2, yPos+1), 2, colors[1], None, 0)
    
def Clear(draw, xPos, yPos, colors, isDaytime):
    if isDaytime:
        Sun(draw, xPos, yPos, colors)
    else:
        Moon(draw, xPos, yPos, colors)
        Stars(draw, xPos, yPos, colors)
        
def SemiCloudy(draw, xPos, yPos, colors, isDaytime):
    if isDaytime:
        Sun(draw, xPos, yPos, colors)
    else:
        Moon(draw, xPos, yPos, colors)
    
    SmallCloud(draw, xPos, yPos, colors)
    
def MostlyCloudy(draw, xPos, yPos, colors, isDaytime):
    if isDaytime:
        SmallSun(draw, xPos, yPos, colors)
    else:
        SmallMoon(draw, xPos, yPos, colors)
    
    Overcast(draw, xPos, yPos, colors)
    
def Showers(draw, xPos, yPos, colors):
    CloudWGap(draw, xPos, yPos, colors)
    
    draw.line([(xPos-16, yPos+30), (xPos-32, yPos+58)], fill=colors[1], width=5)  #line1
    draw.line([(xPos-2, yPos+30), (xPos-22, yPos+65)], fill=colors[1], width=5)  #line2
    draw.line([(xPos+12, yPos+30), (xPos-4, yPos+58)], fill=colors[1], width=5)  #line3
    draw.line([(xPos+26, yPos+30), (xPos-2, yPos+79)], fill=colors[1], width=5)  #line4
    
    Circle(draw, (xPos-16, yPos+30), 2, colors[1], None, 0), Circle(draw, (xPos-32, yPos+58), 2, colors[1], None, 0)
    Circle(draw, (xPos-2, yPos+30), 2, colors[1], None, 0), Circle(draw, (xPos-22, yPos+65), 2, colors[1], None, 0)
    Circle(draw, (xPos+12, yPos+30), 2, colors[1], None, 0), Circle(draw, (xPos-4, yPos+58), 2, colors[1], None, 0)
    Circle(draw, (xPos+26, yPos+30), 2, colors[1], None, 0), Circle(draw, (xPos-2, yPos+79), 2, colors[1], None, 0)
    
def Rain(draw, xPos, yPos, colors):
    CloudWGap(draw, xPos, yPos, colors)
    # Rule is x-4 for y+7 to move down
    
    draw.line([(xPos-20, yPos+37), (xPos-28, yPos+51)], fill=colors[1], width=5)	#line1
    draw.line([(xPos+2, yPos+23), (xPos-6, yPos+37)], fill=colors[1], width=5)		#line2
    draw.line([(xPos-18, yPos+58), (xPos-26, yPos+72)], fill=colors[1], width=5)	#line2b
    draw.line([(xPos+4, yPos+44), (xPos-4, yPos+58)], fill=colors[1], width=5)		#line3
    draw.line([(xPos+26, yPos+30), (xPos+18, yPos+44)], fill=colors[1], width=5)	#line4
    draw.line([(xPos+6, yPos+65), (xPos-2, yPos+79)], fill=colors[1], width=5)		#line4b
    
    Circle(draw, (xPos-20, yPos+37), 2, colors[1], None, 0), Circle(draw, (xPos-28, yPos+51), 2, colors[1], None, 0)
    Circle(draw, (xPos+2, yPos+23), 2, colors[1], None, 0), Circle(draw, (xPos-6, yPos+37), 2, colors[1], None, 0)
    Circle(draw, (xPos-18, yPos+58), 2, colors[1], None, 0), Circle(draw, (xPos-26, yPos+72), 2, colors[1], None, 0)
    Circle(draw, (xPos+4, yPos+44), 2, colors[1], None, 0), Circle(draw, (xPos-4, yPos+58), 2, colors[1], None, 0)
    Circle(draw, (xPos+26, yPos+30), 2, colors[1], None, 0), Circle(draw, (xPos+18, yPos+44), 2, colors[1], None, 0)
    Circle(draw, (xPos+6, yPos+65), 2, colors[1], None, 0), Circle(draw, (xPos-2, yPos+79), 2, colors[1], None, 0)
    
def TOBENAMED(draw, xPos, yPos, colors):
    CloudWGap(draw, xPos, yPos, colors)
    # Rule is x-4 for y+7 to move down
    
    draw.line([(xPos-12, yPos+23), (xPos-20, yPos+37)], fill=colors[1], width=5)	#line1
    draw.line([(xPos-11, yPos+58), (xPos-19, yPos+72)], fill=colors[1], width=5)    #line5
    draw.line([(xPos+22, yPos+37), (xPos+14, yPos+51)], fill=colors[1], width=5)    #line3
    
    draw.line([(xPos+5, yPos+30), (xPos-3, yPos+44)], fill=colors[1], width=5)      #line2
    draw.line([(xPos+8, yPos+41), (xPos-6, yPos+33)], fill=colors[1], width=5)      #cross1
    
    draw.line([(xPos-28, yPos+51), (xPos-36, yPos+65)], fill=colors[1], width=5)	#line4
    draw.line([(xPos-25, yPos+62), (xPos-39, yPos+54)], fill=colors[1], width=5)    #cross2
    
    draw.line([(xPos+6, yPos+65), (xPos-2, yPos+79)], fill=colors[1], width=5)      #line6
    draw.line([(xPos+9, yPos+76), (xPos-5, yPos+68)], fill=colors[1], width=5)      #cross3
    
    Circle(draw, (xPos-12, yPos+23), 2, colors[1], None, 0), Circle(draw, (xPos-20, yPos+37), 2, colors[1], None, 0)
    Circle(draw, (xPos-11, yPos+58), 2, colors[1], None, 0), Circle(draw, (xPos-19, yPos+72), 2, colors[1], None, 0)
    Circle(draw, (xPos+22, yPos+37), 2, colors[1], None, 0), Circle(draw, (xPos+14, yPos+51), 2, colors[1], None, 0)
    
    Circle(draw, (xPos+5, yPos+30), 2, colors[1], None, 0), Circle(draw, (xPos-3, yPos+44), 2, colors[1], None, 0)
    Circle(draw, (xPos+8, yPos+41), 2, colors[1], None, 0), Circle(draw, (xPos-6, yPos+33), 2, colors[1], None, 0)
    
    Circle(draw, (xPos-28, yPos+51), 2, colors[1], None, 0), Circle(draw, (xPos-36, yPos+65), 2, colors[1], None, 0)
    Circle(draw, (xPos-25, yPos+62), 2, colors[1], None, 0), Circle(draw, (xPos-39, yPos+54), 2, colors[1], None, 0)
    
    Circle(draw, (xPos+6, yPos+65), 2, colors[1], None, 0), Circle(draw, (xPos-2, yPos+79), 2, colors[1], None, 0)
    Circle(draw, (xPos+9, yPos+76), 2, colors[1], None, 0), Circle(draw, (xPos-5, yPos+68), 2, colors[1], None, 0)

def ALSOTOBENAMED(draw, xPos, yPos, colors):
    CloudWGap(draw, xPos, yPos, colors)
    # Rule is x-4 for y+7 to move down
    
    draw.line([(xPos-12, yPos+23), (xPos-28, yPos+51)], fill=colors[1], width=5)	#line1
    draw.line([(xPos+5, yPos+30), (xPos+1, yPos+37)], fill=colors[1], width=5)      #line2
    draw.line([(xPos+22, yPos+37), (xPos+10, yPos+58)], fill=colors[1], width=5)    #line3
    draw.line([(xPos-15, yPos+65), (xPos-23, yPos+79)], fill=colors[1], width=5)    #line4
    
    Circle(draw, (xPos-7, yPos+51), 4, colors[1], None, 0)
    Circle(draw, (xPos-36, yPos+65), 4, colors[1], None, 0)
    Circle(draw, (xPos-31, yPos+93), 4, colors[1], None, 0)
    Circle(draw, (xPos+2, yPos+72), 4, colors[1], None, 0)
    
    Circle(draw, (xPos-12, yPos+23), 2, colors[1], None, 0), Circle(draw, (xPos-28, yPos+51), 2, colors[1], None, 0)
    Circle(draw, (xPos+5, yPos+30), 2, colors[1], None, 0), Circle(draw, (xPos+1, yPos+37), 2, colors[1], None, 0)
    Circle(draw, (xPos+22, yPos+37), 2, colors[1], None, 0), Circle(draw, (xPos+10, yPos+58), 2, colors[1], None, 0)
    Circle(draw, (xPos-15, yPos+65), 2, colors[1], None, 0), Circle(draw, (xPos-23, yPos+79), 2, colors[1], None, 0)
    
def ALSOALSOTOBENAMED(draw, xPos, yPos, colors):
    CloudWGap(draw, xPos, yPos, colors)
    # Rule is x-4 for y+7 to move down
    
    draw.line([(xPos-9, yPos+29), (xPos-17, yPos+43)], fill=colors[1], width=5)     #line1
    draw.line([(xPos-6, yPos+40), (xPos-20, yPos+32)], fill=colors[1], width=5)     #cross1
    
    draw.line([(xPos+19, yPos+33), (xPos+11, yPos+47)], fill=colors[1], width=5)    #line2
    draw.line([(xPos+22, yPos+44), (xPos+8, yPos+36)], fill=colors[1], width=5)     #cross2
    
    draw.line([(xPos-25, yPos+53), (xPos-33, yPos+67)], fill=colors[1], width=5)    #line3
    draw.line([(xPos-22, yPos+64), (xPos-36, yPos+56)], fill=colors[1], width=5)    #cross3
    
    draw.line([(xPos+3, yPos+57), (xPos-5, yPos+71)], fill=colors[1], width=5)      #line4
    draw.line([(xPos+6, yPos+68), (xPos-8, yPos+60)], fill=colors[1], width=5)      #cross4
    
    Circle(draw, (xPos-9, yPos+29), 2, colors[1], None, 0), Circle(draw, (xPos-17, yPos+43), 2, colors[1], None, 0)
    Circle(draw, (xPos-6, yPos+40), 2, colors[1], None, 0), Circle(draw, (xPos-20, yPos+32), 2, colors[1], None, 0)
    Circle(draw, (xPos+19, yPos+33), 2, colors[1], None, 0), Circle(draw, (xPos+11, yPos+47), 2, colors[1], None, 0)
    Circle(draw, (xPos+22, yPos+44), 2, colors[1], None, 0), Circle(draw, (xPos+8, yPos+36), 2, colors[1], None, 0)
    Circle(draw, (xPos-25, yPos+53), 2, colors[1], None, 0), Circle(draw, (xPos-33, yPos+67), 2, colors[1], None, 0)
    Circle(draw, (xPos-22, yPos+64), 2, colors[1], None, 0), Circle(draw, (xPos-36, yPos+56), 2, colors[1], None, 0)
    Circle(draw, (xPos+3, yPos+57), 2, colors[1], None, 0), Circle(draw, (xPos-5, yPos+71), 2, colors[1], None, 0)
    Circle(draw, (xPos+6, yPos+68), 2, colors[1], None, 0), Circle(draw, (xPos-8, yPos+60), 2, colors[1], None, 0)

def New(draw, xPos, yPos, colors):
    CloudWGap(draw, xPos, yPos, colors)
    
    draw.line([(xPos-30, yPos+27), (xPos-9, yPos+55)], fill=colors[1], width=5)
    
    draw.line([(xPos-30, yPos+55), (xPos-9, yPos+55)], fill=colors[1], width=5)
    draw.line([(xPos+7, yPos+55), (xPos+32, yPos+55)], fill=colors[1], width=5)
    